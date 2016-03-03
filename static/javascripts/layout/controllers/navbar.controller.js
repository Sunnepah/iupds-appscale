/**
* NavbarController
* @namespace iupds.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('iupds.layout.controllers')
    .controller('NavbarController', NavbarController);

  NavbarController.$inject = ['$scope', '$cookies', 'Authentication'];

  /**
  * @namespace NavbarController
  */
  function NavbarController($scope, $cookies, Authentication) {
    var vm = this;

    vm.logout = logout;

    // vm.nickname = JSON.parse($cookies.authenticatedAccount).user.nickname;
    // console.log(vm.nickname);
    // return vm.nickname
    /**
    * @name logout
    * @desc Log the user out
    * @memberOf iupds.layout.controllers.NavbarController
    */
    function logout() {
      Authentication.logout();
    }
  }
})();