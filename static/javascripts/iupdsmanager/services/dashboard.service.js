/**
* Dashboard
* @namespace iupds.iupdsmanager.service
*/
(function () {
    'use strict';

    angular
      .module('iupds.iupdsmanager.services')
      .factory('Dashboard', Dashboard);

    Dashboard.$inject = ['$cookies', '$http', 'Authentication'];

    /**
    * @namespace Dashboard
    * @return {Factory}
    */
    function Dashboard($cookies, $http, Authentication) {
        /**
        * @name Dashboard
        * @desc The Factory to be returned
        */
        var Dashboard = {

            getCurrentUserProfile: getCurrentUserProfile,
            register: register,
            getGraphCount: getGraphCount,
            createGraphs: createGraphs,
            dropGraphs: dropGraphs,

        };

        return Dashboard;

        ////////Service Functions/////////

        /**
        */
        function getCurrentUserProfile() {
            return $http.get('/api/v1/user/profile/', {
            }).then(successFn, failureFn);
        }

        function successFn(data, status, headers, config) {

            if(data.status == 200 && data.data.user.user_id && data.data.user.email) {
                Authentication.setAuthenticatedAccount(data.data);
            }
        }

        function failureFn(data, status, headers, config) {
            console.error('Error occurred');
        }

        function getGraphCount() {
                //return $http.get('/api/v1/profile/', {
                //}).then(successGraphFn, failureGraphFn);

                $http.get('/api/v1/user/profile/')
                          .then(function(result) {
                            console.log(result.data);
                });
        }

        function successGraphFn(data, status, headers, config) {

            if(data.status == 200 && data.data.user.user_id && data.data.user.email) {
                //return data.data;
            }
        }

        function failureGraphFn(data, status, headers, config) {
            console.error('Error occurred');
        }

        /**
        * @name register
        * @desc Try to register a new user
        * @param {string} password The password entered by the user
        * @param {string} email The email entered by the user
        * @param password_confirmation
        * @returns {Promise}
        * @memberOf iupds.iupdsmanager.services.Dashboard
        */
        function register(email, password, password_confirmation) {

            $http({
                url: "/api/v1/user/",
                dataType: "json",
                method: "POST",
                data:{email: email,password: password,password_confirmation: password_confirmation },
                headers: {
                    "Content-Type": "application/json"
                }
            }).success(function(response){
                console.log(response);
            }).error(function(error){
                console.log(error);
            });
        }

        function createGraphs() {

            $http({
                url: "/api/v1/graph/user/",
                dataType: "json",
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                }
            }).success(function(response){
                console.log(response);
            }).error(function(error){
                console.log(error);
            });

            $http({
                url: "/api/v1/user/graph/create",
                dataType: "json",
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                }
            }).success(function(response){
                console.log(response);
            }).error(function(error){
                console.log(error);
            });
        }

        function dropGraphs() {

            $http({
                url: "/api/v1/user/graph/drop/",
                dataType: "json",
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                }
            }).success(function(response){
                console.log(response);
            }).error(function(error){
                console.log(error);
            });
        }


    } //end Factory
})();