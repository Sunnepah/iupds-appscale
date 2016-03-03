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
            register: register

        };

        return Dashboard;

        ////////Service Functions/////////

        /**
        */
        function getCurrentUserProfile() {
            return $http.get('/api/v1/profile/', {
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

        /**
        * @name register
        * @desc Try to register a new user
        * @param {string} password The password entered by the user
        * @param {string} email The email entered by the user
        * @returns {Promise}
        * @memberOf iupds.iupdsmanager.services.Dashboard
        */
        function register(email, password, password_confirmation) {

            $http({
                url: "/api/v1/create_user/",
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
//          return $http.post('/api/v1/create_user/', {
//            email: email,
//            password: password,
//            password_confirmation: password_confirmation
//          }).then(registerSuccessFn, registerErrorFn);
//
//          /**
//          * @name registerSuccessFn
//          * @desc
//          */
//          function registerSuccessFn(data, status, headers, config) {
//            console.log(data);
//          }
//
//          /**
//          * @name registerErrorFn
//          * @desc Log "Oops! failure!" to the console
//          */
//          function registerErrorFn(data, status, headers, config) {
//            console.error('Oops!, failure!');
//          }

    }


    } //end Factory
})();