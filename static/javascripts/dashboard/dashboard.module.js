(function () {
  'use strict';

  angular
    .module('iupds.dashboard', [
      'iupds.dashboard.controllers',
      'iupds.dashboard.services'
    ]);

  angular
    .module('iupds.dashboard.controllers', []);

  angular
    .module('iupds.dashboard.services', ['ngCookies']);
})();