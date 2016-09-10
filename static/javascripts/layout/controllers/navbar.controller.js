/**
* NavbarController
* @namespace iupds.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('iupds.layout.controllers')
    .controller('NavbarController', NavbarController);

  NavbarController.$inject = ['Authentication'];

  /**
  * @namespace NavbarController
  */
  function NavbarController(Authentication) {
    var vm = this;

    vm.logout = logout;

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