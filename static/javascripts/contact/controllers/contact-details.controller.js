/**
* ContactDetailsController
* @namespace iupds.contact-details.controllers
*/
(function () {
  'use strict';

  angular
    .module('iupds.contact.controllers')
    .controller('ContactDetailsController', ContactDetailsController);

  ContactDetailsController.$inject = ['$location', '$routeParams', 'Profile', 'Snackbar', 'Authentication', 'Dashboard', 'Contact'];

  /**
  * @namespace ContactDetailsController
  */
  function ContactDetailsController($location, $routeParams, Profile, Snackbar, Authentication, Dashboard, Contact) {
    var vm = this;

    vm.getContactDetails = getContactDetails;
    vm.contacts = [];
    vm.user = []

    activate();
    //vm.contacts =
    getContactDetails()

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
//      else {
//        // Redirect if logged in, but not the owner of this profile.
//        if (authenticatedAccount.username !== username) {
//          $location.url('/');
//          Snackbar.error('You are not authorized to view this page.');
//        }
//      }
    }


    /**
    * @name getContactDetails
    * @desc Get this user's contact details
    * @memberOf iupds.contact.controllers.ContactDetailsController
    */
    function getContactDetails() {
      // activate();
      Contact.getContactDetails().then(SuccessFn, FailureFn);

      /**
      * @name profileSuccessFn
      * @desc Show success snackbar
      */
      function SuccessFn(data, status, headers, config) {
         vm.contacts = data.data;
         console.log(vm.contacts);
         Snackbar.show('Success.');
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