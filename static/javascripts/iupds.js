(function () {
  'use strict';

  angular
    .module('iupds', [
      'iupds.config',
      'iupds.routes',
      'iupds.authentication',
      'iupds.layout',
      'iupds.iupdsmanager',
      'iupds.profiles',
      'iupds.utils',
      'iupds.contact'
    ]);

  angular
    .module('iupds.routes', ['ngRoute']);

  angular
    .module('iupds.config', []);

  angular
    .module('iupds')
    .run(run);

  run.$inject = ['$http'];

    /**
    * @name run
    * @desc Update xsrf $http headers to align with Django's defaults
    */
    function run($http) {
      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';
    }
})();