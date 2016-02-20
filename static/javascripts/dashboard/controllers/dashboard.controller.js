/**
* Dashboard controller
* @namespace iupds.dashboard.controllers
*/

(function () {
    'use strict';

    angular
      .module('iupds.dashboard.controllers')
      .controller('DashboardController', DashboardController);

    DashboardController.$inject = ['$location', '$scope', 'Dashboard'];

    /**
    * @namespace DashboardController
    */
    function DashboardController($location, $scope, Dashboard) {
        var vm = this;

        vm.profile = profile;
        profile();
        /**
        * @name profile
        * @desc Display user profile
        * @memberOf iupds.dashboard.controllers.DashboardController
        */
        function profile() {
          console.log("here");
          Dashboard.getCurrentUserProfile();
        }
    }

})();