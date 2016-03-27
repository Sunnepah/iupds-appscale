/**
* Dashboard
* @namespace iupds.contact.service
*/
(function () {
    'use strict';

    angular
      .module('iupds.contact.services')
      .factory('Contact', Contact);

    Contact.$inject = ['$cookies', '$http'];

    /**
    * @namespace Contact
    * @return {Factory}
    */
    function Contact($cookies, $http) {
        /**
        * @name Contact
        * @desc The Factory to be returned
        */
        var Contact = {

            createContact: createContact,
            getContactDetails: getContactDetails

        };

        return Contact;

        ////////Service Functions/////////

        /**
        */

        function createContact(contact) {
                return $http.post('/api/v1/contact/', contact);
        }

        function getContactDetails() {
                return $http.get('/api/v1/contact/details');
        }

    } //end Factory
})();