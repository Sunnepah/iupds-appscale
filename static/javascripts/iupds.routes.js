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
      templateUrl: '/static/templates/iupdsmanager/dashboard.html'
    }).when('/profileold', {
      controller: 'DashboardController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/iupdsmanager/profile.html'
    }).when('/register', {
      controller: 'DashboardController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/iupdsmanager/register.html'
    }).when('/login', {
      controller: 'LoginController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/login.html'
    }).when('/profile', {
      controller: 'ProfileController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/iupdsmanager/profile.html',
      sp: {
        authenticate: true
      }
    }).when('/profile/settings', {
      controller: 'ProfileSettingsController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/iupdsmanager/settings.html',
      sp: {
        authenticate: true
      }
    }).otherwise('/', {
      controller: 'DashboardController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/dashboard/dashboard.html'
    });
  }
})();