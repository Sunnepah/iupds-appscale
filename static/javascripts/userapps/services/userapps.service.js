/**
* Userapps
* @namespace iupds.Userapps.service
*/
(function () {
    'use strict';

    angular
      .module('iupds.userapps.services')
      .factory('Userapps', Userapps);

    Userapps.$inject = ['$cookies', '$http'];

    /**
    * @namespace Userapps
    * @return {Factory}
    */
    function Userapps($cookies, $http) {
        /**
        * @name Userapps
        * @desc The Factory to be returned
        */
        var Userapps = {
            getUserConnectedApps: getUserConnectedApps,
            revokeConnectedAppsAccess: revokeConnectedAppsAccess
        };

        return Userapps;

        ////////Service Functions/////////

        /**
        */
        function getUserConnectedApps() {
            return $http.get('/api/v1/user/applications/');
        }

        /**
         */
        function revokeConnectedAppsAccess(client_id) {
            return $http.delete('/api/v1/user/applications/'+client_id+'/');
        }

    } //end Factory
})();