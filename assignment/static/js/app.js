angular.module('app', [])
    .controller('main-controller', function ($scope, $http, $log) {
        $http.get('/states').then(function (response) {
            $scope.constituencies_visible = false;
            $scope.main_region = response.data.main_region;
            $scope.states = response.data.sub_regions;
        }, function (response) {
            $log.log(response)
        });
        $scope.show_constituencies = function (state) {

            $http.get('/states/'+ state.name + '/constituencies').then(function (response) {
                $scope.constituencies_visible = true;
                $scope.constituencies = response.data.constituencies;
            }, function (response) {
                $log.log(response)
            });
        }
    });