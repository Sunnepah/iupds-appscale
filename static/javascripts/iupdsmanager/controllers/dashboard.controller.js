/**
* Dashboard controller
* @namespace iupds.iupdsmanager.controllers
*/

(function () {
    'use strict';

    angular
      .module('iupds.iupdsmanager.controllers')
      .controller('DashboardController', DashboardController);

    DashboardController.$inject = ['$location', '$scope', '$cookies', '$http', 'Dashboard', 'Authentication'];

    /**
    * @namespace DashboardController
    */
    function DashboardController($location, $scope, $cookies,$http, Dashboard, Authentication) {
        var vm = this;

        vm.getProfile = getProfile;
        vm.user = [];
        vm.register = register;
        vm.contact_graph = [];
        vm.graphs = 1;
        vm.createGraphs = createGraphs;
        vm.dropGraphs = dropGraphs;

        // If the user is authenticated, they should not be here.
        if (Authentication.isAuthenticated()) {
            vm.user = Authentication.getAuthenticatedAccount()
        } else {
            getProfile();
            vm.user = Authentication.getAuthenticatedAccount()
        }

        // console.log(vm.user);
        //vm.data = Dashboard.getGraphCount();
        //console.log(vm.data);
        //vm.data = [];
        $http.get('/api/v1/profile/')
          .then(function(result) {
            vm.data = result.data;
            vm.contact_graph = vm.data.contact_graph;
            console.log(vm.data);
        });


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

        function createGraphs() {
            Dashboard.createGraphs();
        }

        function dropGraphs() {
            Dashboard.dropGraphs();
        }
    }

})();