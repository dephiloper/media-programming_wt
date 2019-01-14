angular.module('app', ['chart.js'])
    .controller('main-controller', function ($scope, $http, $log) {
        $http.get('/states').then(function (response) {
            $scope.constituencies_visible = false;
            $scope.main_region = response.data.main_region;
            $scope.states = response.data.sub_regions;
        }, function (response) {
            $log.log(response)
        });

        $scope.show_constituencies = function ($event, state) {
            $http.get('/states/' + state.id + '/constituencies/')
                .then(function (response) {
                    $scope.constituencies_visible = true;
                    $scope.votes_visible = false;
                    $scope.constituencies = response.data.constituencies;
                    $scope.state = state;
                    //let element = angular.element($event.target);
                    //element.addClass("active");
                }, function (response) {
                    $log.log(response)
                });
        };

        $scope.show_votes = function ($event, constituency) {
            $http.get('/states/' + $scope.state.id + '/constituencies/' + constituency.id + "/votes/")
                .then(function (response) {
                    $scope.votes_visible = true;

                    $scope.votes = response.data.votes;
                    $scope.max_temp = $scope.votes[0].temporary_result;
                    $scope.second_max_temp = $scope.votes[0].second_temporary_result;

                    // remove the first 4 rows
                    $scope.votes = $scope.votes.slice(4);

                    // sort the result
                    $scope.votes.sort((a, b) =>
                        ((b.temporary_result + b.second_temporary_result) - (a.temporary_result + a.second_temporary_result)));

                    $scope.constituency = constituency;


                    // charts
                    $scope.votes_data = [$scope.votes.map(v=>v.temporary_result), $scope.votes.map(v=>v.second_temporary_result)];
                    $scope.votes_labels =$scope.votes.map(v=>v.party.substr(0, 10));
                    $scope.votes_series = ["Erststimmen", "Zweitstimmen"];

                    $scope.first_votes_labels = $scope.votes.map(value => value.party);
                    $scope.first_votes_data = $scope.votes.map(value => parseInt(value.temporary_result));
                    $scope.second_votes_labels = $scope.votes.map(value => value.party);
                    $scope.second_votes_data = $scope.votes.map(value => parseInt(value.second_temporary_result));

                }, function (response) {
                    $log.log(response)
                });
        };
    });