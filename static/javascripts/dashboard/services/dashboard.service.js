/**
* Dashboard
* @namespace iupds.dashboard.service
*/
(function () {
    'use strict';

    angular
      .module('iupds.dashboard.services')
      .factory('Dashboard', Dashboard);

    Dashboard.$inject = ['$cookies', '$http'];

    /**
    * @namespace Dashboard
    * @return {Factory}
    */
    function Dashboard($cookies, $http) {
        /**
        * @name Dashboard
        * @desc The Factory to be returned
        */
        var Dashboard = {

            getCurrentUserProfile: getCurrentUserProfile

        };

        return Dashboard;

        ////////Service Functions/////////

        /**
        */
        function getCurrentUserProfile() {
            return $http.get('/api/v1/profiles/', {
            }).then(successFn, failureFn);
        }

        function successFn(data, status, headers, config) {
            console.log('Success');
        }

        function failureFn(data, status, headers, config) {
            console.error('Error occurred');
        }


    } //end Factory
})();