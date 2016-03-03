/**
* Dashboard controller
* @namespace iupds.iupdsmanager.controllers
*/

(function () {
    'use strict';

    angular
      .module('iupds.iupdsmanager.controllers')
      .controller('DashboardController', DashboardController);

    DashboardController.$inject = ['$location', '$scope', '$cookies', 'Dashboard', 'Authentication'];

    /**
    * @namespace DashboardController
    */
    function DashboardController($location, $scope, $cookies, Dashboard, Authentication) {
        var vm = this;

        vm.getProfile = getProfile;
        vm.user = [];
        vm.register = register;

        // If the user is authenticated, they should not be here.
        if (Authentication.isAuthenticated()) {
            vm.user = Authentication.getAuthenticatedAccount()
        } else {
            getProfile();
            vm.user = Authentication.getAuthenticatedAccount()
        }

        return vm.user;

        /**
        * @name profile
        * @desc Display user profile
        * @memberOf iupds.iupdsmanager.controllers.DashboardController
        */
        function getProfile() {
          Dashboard.getCurrentUserProfile();
        }

        /**
        * @name register
        * @desc Register a new user
        * @memberOf iupds.iupdsmanager.controllers.DashboardController
        */
        function register() {
          Dashboard.register('jade@gmail.com', '1234567', '1234567');
        }
    }

})();