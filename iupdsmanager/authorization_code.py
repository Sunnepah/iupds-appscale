# -*- coding: utf-8 -*-
"""
Extends oauthlib.oauth2.rfc6749.grant_types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from __future__ import unicode_literals, absolute_import

import logging

from oauthlib import common
from oauthlib.oauth2 import AuthorizationCodeGrant
from oauthlib.oauth2 import FatalClientError, OAuth2Error, InvalidRequestFatalError,MissingClientIdError, InvalidClientIdError, \
    InvalidRedirectURIError, MismatchingRedirectURIError, MissingRedirectURIError, \
    MissingResponseTypeError, UnsupportedResponseTypeError, UnauthorizedClientError

from oauthlib.uri_validate import is_absolute_uri
from iupdsmanager.oauth2_validators import OAuth2Validator

log = logging.getLogger(__name__)
request_validator = OAuth2Validator()


class AuthorizationCodeGrantPds(AuthorizationCodeGrant):

    def create_authorization_response(self, request, token_handler):

        try:
            # request.scopes is only mandated in post auth and both pre and
            # post auth use validate_authorization_request
            # if not request.scopes:
            #     raise ValueError('Scopes must be set on post auth.')

            # self.validate_authorization_request(request)
            log.debug('Pre resource owner authorization validation ok for %r.',
                      request)

        # If the request fails due to a missing, invalid, or mismatching
        # redirection URI, or if the client identifier is missing or invalid,
        # the authorization server SHOULD inform the resource owner of the
        # error and MUST NOT automatically redirect the user-agent to the
        # invalid redirection URI.
        except FatalClientError as e:
            log.debug('Fatal client error during validation of %r. %r.',
                      request, e)
            raise

        # If the resource owner denies the access request or if the request
        # fails for reasons other than a missing or invalid redirection URI,
        # the authorization server informs the client by adding the following
        # parameters to the query component of the redirection URI using the
        # "application/x-www-form-urlencoded" format, per Appendix B:
        # http://tools.ietf.org/html/rfc6749#appendix-B
        except OAuth2Error as e:
            log.debug('Client error during validation of %r. %r.', request, e)
            request.redirect_uri = request.redirect_uri or self.error_uri
            return {'Location': common.add_params_to_uri(request.redirect_uri, e.twotuples)}, None, 302

        grant = self.create_authorization_code(request)
        log.debug('Saving grant %r for %r.', grant, request)

        request_validator.save_authorization_code(request.client_id, grant, request)
        return {'Location': common.add_params_to_uri(request.redirect_uri, grant.items())}, None, 302

    def validate_authorization_request(self, request):
        """Check the authorization request for normal and fatal errors.

        A normal error could be a missing response_type parameter or the client
        attempting to access scope it is not allowed to ask authorization for.
        Normal errors can safely be included in the redirection URI and
        sent back to the client.

        Fatal errors occur when the client_id or redirect_uri is invalid or
        missing. These must be caught by the provider and handled, how this
        is done is outside of the scope of OAuthLib but showing an error
        page describing the issue is a good idea.
        """

        # First check for fatal errors

        # If the request fails due to a missing, invalid, or mismatching
        # redirection URI, or if the client identifier is missing or invalid,
        # the authorization server SHOULD inform the resource owner of the
        # error and MUST NOT automatically redirect the user-agent to the
        # invalid redirection URI.

        # First check duplicate parameters
        for param in ('client_id', 'response_type', 'redirect_uri', 'scope', 'state'):
            try:
                duplicate_params = request.duplicate_params
            except ValueError:
                raise InvalidRequestFatalError(description='Unable to parse query string', request=request)
            if param in duplicate_params:
                raise InvalidRequestFatalError(description='Duplicate %s parameter.' % param, request=request)

        # REQUIRED. The client identifier as described in Section 2.2.
        # http://tools.ietf.org/html/rfc6749#section-2.2
        if not request.client_id:
            raise MissingClientIdError(request=request)

        if not request_validator.validate_client_id(request.client_id, request):
            raise InvalidClientIdError(request=request)

        # OPTIONAL. As described in Section 3.1.2.
        # http://tools.ietf.org/html/rfc6749#section-3.1.2
        log.debug('Validating redirection uri %s for client %s.',
                  request.redirect_uri, request.client_id)
        if request.redirect_uri is not None:
            request.using_default_redirect_uri = False
            log.debug('Using provided redirect_uri %s', request.redirect_uri)
            if not is_absolute_uri(request.redirect_uri):
                raise InvalidRedirectURIError(request=request)

            if not request_validator.validate_redirect_uri(
                    request.client_id, request.redirect_uri, request):
                raise MismatchingRedirectURIError(request=request)
        else:
            request.redirect_uri = request_validator.get_default_redirect_uri(
                request.client_id, request)
            request.using_default_redirect_uri = True
            log.debug('Using default redirect_uri %s.', request.redirect_uri)
            if not request.redirect_uri:
                raise MissingRedirectURIError(request=request)

        # Then check for normal errors.

        # If the resource owner denies the access request or if the request
        # fails for reasons other than a missing or invalid redirection URI,
        # the authorization server informs the client by adding the following
        # parameters to the query component of the redirection URI using the
        # "application/x-www-form-urlencoded" format, per Appendix B.
        # http://tools.ietf.org/html/rfc6749#appendix-B

        # Note that the correct parameters to be added are automatically
        # populated through the use of specific exceptions.

        # REQUIRED.
        if request.response_type is None:
            raise MissingResponseTypeError(request=request)
        # Value MUST be set to "code".
        elif request.response_type != 'code':
            raise UnsupportedResponseTypeError(request=request)

        if not request_validator.validate_response_type(request.client_id,
                                                             request.response_type,
                                                             request.client, request):
            log.debug('Client %s is not authorized to use response_type %s.',
                      request.client_id, request.response_type)
            raise UnauthorizedClientError(request=request)

        # OPTIONAL. The scope of the access request as described by Section 3.3
        # http://tools.ietf.org/html/rfc6749#section-3.3
        self.validate_scopes(request)

        return request.scopes, {
            'client_id': request.client_id,
            'redirect_uri': request.redirect_uri,
            'response_type': request.response_type,
            'state': request.state,
            'request': request,
        }

    def save_authorization_client_code(self, request, grant):
        request_validator.save_authorization_code(request.client_id, grant, request)

    def save_bearer_token(self, token, request):
        request_validator.save_bearer_token(token, request)

    def revoke_token(self, token, token_type_hint, request):
        request_validator.revoke_token(token, token_type_hint, request)


