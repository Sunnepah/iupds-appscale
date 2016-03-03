/**
* ProfileController
* @namespace iupds.profiles.controllers
*/
(function () {
  'use strict';

  angular
    .module('iupds.profiles.controllers')
    .controller('ProfileController', ProfileController);

  ProfileController.$inject = ['$location', '$routeParams', 'Profile', 'Snackbar', 'Authentication', 'Dashboard'];

  /**
  * @namespace ProfileController
  */
  function ProfileController($location, $routeParams, Profile, Snackbar, Authentication, Dashboard) {
    var vm = this;

    vm.profile = undefined;
    vm.user = []

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf iupds.profiles.controllers.ProfileController
    */
    function activate() {

      if (Authentication.isAuthenticated()) {
          vm.user = Authentication.getAuthenticatedAccount()
      } else {
          Dashboard.getCurrentUserProfile();
          vm.user = Authentication.getAuthenticatedAccount()
      }

      Profile.get(vm.user.user['email']).then(profileSuccessFn, profileErrorFn);

      /**
      * @name profileSuccessProfile
      * @desc Update `profile` on viewmodel
      */
      function profileSuccessFn(data, status, headers, config) {
        vm.profile = data.data.user;
        console.log(vm.profile);
      }


      /**
      * @name profileErrorFn
      * @desc Redirect to index and show error Snackbar
      */
      function profileErrorFn(data, status, headers, config) {
        $location.url('/');
        Snackbar.error('That user does not exist.');
      }


      /**
        * @name postsSucessFn
        * @desc Update `posts` on viewmodel
        */
      function postsSuccessFn(data, status, headers, config) {
        vm.posts = data.data;
      }


      /**
        * @name postsErrorFn
        * @desc Show error snackbar
        */
      function postsErrorFn(data, status, headers, config) {
        Snackbar.error(data.data.error);
      }
    }
  }
})();