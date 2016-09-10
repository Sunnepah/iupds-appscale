/**
* ProfileController
* @namespace iupds.contact.controllers
*/
(function () {
  'use strict';

  angular
    .module('iupds.contact.controllers')
    .controller('ContactController', ContactController);

  ContactController.$inject = ['$location', '$routeParams', 'Profile', 'Snackbar', 'Authentication', 'Dashboard', 'Contact'];

  /**
  * @namespace ContactController
  */
  function ContactController($location, $routeParams, Profile, Snackbar, Authentication, Dashboard, Contact) {
    var vm = this;

    vm.createContact = createContact;
    vm.contact = [];
    vm.user = []

    vm.contact = {'email': '',
                  'telephone': '',
                  'telephone_type': 'Mobile',
                  'street1': '',
                  'street2': '',
                  'city': '',
                  'post_code': '',
                  'country': ''};

     /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated.
    * @memberOf iupds.profiles.controllers.ContactController
    */
    function activate() {
          var authenticatedAccount = Authentication.getAuthenticatedAccount();

          // Redirect if not logged in
          if (!authenticatedAccount) {
            Authentication.logout();
            Snackbar.error('You are not authorized to view this page.');
          }
          else {
            // Redirect if logged in, but not the owner of this profile.
            if (authenticatedAccount.username !== username) {
                $location.url('/');
                Snackbar.error('You are not authorized to view this page.');
            }
         }
    }

    /**
    * @name updateContact
    * @desc Update this user's contact
    * @memberOf iupds.contact.controllers.ContactController
    */
    function createContact() {
      activate();
      Contact.createContact(vm.contact).then(SuccessFn, FailureFn);

      /**
      * @name profileSuccessFn
      * @desc Show success snackbar
      */
      function SuccessFn(data, status, headers, config) {
         Snackbar.show('Your contact has been updated.');
      }


      /**
      * @name profileErrorFn
      * @desc Show error snackbar
      */
      function FailureFn(data, status, headers, config) {
        Snackbar.error(data.error);
      }

    }

  } //end Factory

})();