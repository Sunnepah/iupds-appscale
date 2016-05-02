/**
* UserappsController
* @namespace iupds.userapps.controllers
*/
(function () {
  'use strict';

  angular
    .module('iupds.userapps.controllers')
    .controller('UserappsController', UserappsController);

  UserappsController.$inject = ['$location', '$routeParams', 'Profile', 'Snackbar', 'Authentication', 'Dashboard', 'Userapps'];

  /**
  * @namespace UserappsController
  */
  function UserappsController($location, $routeParams, Profile, Snackbar, Authentication, Dashboard, Userapps) {
    var vm = this;

    vm.getUserConnectedApps = getUserConnectedApps;
    vm.apps = [];
    vm.user = [];

    vm.revokeAppAccess = revokeAppAccess;

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
    }

    getUserConnectedApps();

    /**
    * @name getUserConnectedApps
    * @desc Get apps connected to this user's data
    * @memberOf iupds.userapps.controllers.UserappsController
    */
    function getUserConnectedApps() {
      activate();
      Userapps.getUserConnectedApps().then(SuccessFn, FailureFn);

      /**
      * @name profileSuccessFn
      * @desc Show success snackbar
      */
      function SuccessFn(data, status, headers, config) {
//         Snackbar.show('Your contact has been updated.');
           vm.apps = data.data.user_applications;
           console.log(vm.apps);
      }


      /**
      * @name profileErrorFn
      * @desc Show error snackbar
      */
      function FailureFn(data, status, headers, config) {
        Snackbar.error(data.error);
      }

    }

    function revokeAppAccess(client_id) {
        Userapps.revokeConnectedAppsAccess(client_id).then(rvSuccess, rvFailure);

        function rvSuccess(data, status, headers, config) {
            getUserConnectedApps();
        }

        function rvFailure(data, status, headers, config) {
            Snackbar.error(data.error);
        }
    }

  } //end Factory

})();