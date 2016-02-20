(function () {
  'use strict';

  angular
    .module('iupds.routes')
    .config(config);

  config.$inject = ['$routeProvider'];

  /**
  * @name config
  * @desc Define valid application routes
  */
  function config($routeProvider) {
    $routeProvider.when('/', {
      controller: 'DashboardController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/dashboard/dashboard.html'
    }).when('/profile', {
      controller: 'DashboardController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/dashboard/profile.html'
    }).when('/register', {
      controller: 'RegisterController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/register.html'
    }).when('/login', {
      controller: 'LoginController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/login.html'
    }).otherwise('/', {
      controller: 'DashboardController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/dashboard/dashboard.html'
    });
  }
})();