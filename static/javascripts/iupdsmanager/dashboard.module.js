(function () {
  'use strict';

  angular
    .module('iupds.iupdsmanager', [
      'iupds.iupdsmanager.controllers',
      'iupds.iupdsmanager.services'
    ]);

  angular
    .module('iupds.iupdsmanager.controllers', []);

  angular
    .module('iupds.iupdsmanager.services', ['ngCookies']);
})();