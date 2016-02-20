/**
* Dashboard controller
* @namespace iupds.dashboard.controllers
*/

(function () {
    'use strict';

    angular
      .module('iupds.dashboard.controllers')
      .controller('DashboardController', DashboardController);

    DashboardController.$inject = ['$location', '$scope'];

    /**
    * @namespace DashboardController
    */
    function DashboardController($location, $scope) {
        var vm = this;

        vm.profile = profile

        /**
        * @name profile
        * @desc Display user profile
        * @memberOf iupds.dashboard.controllers.DashboardController
        */
        function profile() {
          console.log("here");
        }
    }

})();