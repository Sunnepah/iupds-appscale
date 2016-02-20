(function () {
  'use strict';

  angular
    .module('iupds.authentication', [
      'iupds.authentication.controllers',
      'iupds.authentication.services'
    ]);

  angular
    .module('iupds.authentication.controllers', []);

  angular
    .module('iupds.authentication.services', ['ngCookies']);
})();