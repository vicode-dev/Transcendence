// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GameResults {
    struct GameResult {
        uint64 gameId;
        int[] playerIds;
        uint8[] score;
        uint16 duration;
        uint64 startTime;
        uint64 endTime;
    }

    struct Tournament {
        uint32 tournamentId;
        uint64[] gameIds;
        int[] playerIds;
    }

    // Store game results
    GameResult[] public results;
    Tournament[] public tournament;
    address author;
    
    constructor() {
        author = msg.sender;
    }

    // Event to log the addition of a new game result
    event ResultAdded(uint64 gameId, int[] playerIds, uint8[] score, uint64 duration);

    event TournamementAdded(uint32 tournamementId);



    // Function to add a game result
    function addGameResult(uint64 _gameId, int[] memory _playerIds, uint8[] memory _score, uint16 _duration, uint64 _startTime, uint64 _endTime) public {
        // Create a new game result
        GameResult memory newResult = GameResult({
        gameId: _gameId,
        playerIds: _playerIds,
        score: _score,
        duration: _duration,
        startTime: _startTime,
        endTime: _endTime
        });

        // Store the result in the array
        results.push(newResult);

        // Emit an event for the new result
        emit ResultAdded(_gameId, _playerIds, _score, _startTime);
    }

    function addTournamementResult(uint32 _tournamentId, uint64[] memory _gameIds, int[] memory _playerIds) public
    {
        Tournament memory newResult = Tournament({
            tournamentId: _tournamentId,
            gameIds: _gameIds,
            playerIds: _playerIds
        });
        tournament.push(newResult);

        emit TournamementAdded(_tournamentId);
    }

    // Function to get a game result by index
    function getGameResult(uint64 index) public view returns (GameResult memory) {
        require(index < results.length, "Game result does not exist");
        return (results[index]);
    }

    function getPlayerGames(int index) public view returns (GameResult[] memory) {
        uint64 count = 0;
        for (uint i = 0; i < results.length; i++) {
            for (uint j = 0; j < results[i].playerIds.length; j++)
            {
                if(index == results[i].playerIds[j])
                    count++;
            }
        }
        GameResult[] memory games = new GameResult[](count);
        for (uint i = 0; i < results.length; i++) {
            for (uint j = 0; j < results[i].playerIds.length; j++)
            {
                if(index == results[i].playerIds[j])
                    games[--count] = results[i];
            }
        }
        return games;
    }

    function getTournament(uint64 index) public view returns (Tournament memory) {
        require (index < tournament.length, "Tournament does not exist");
        return (tournament[index]);
    }

    // Function to get the total number of game results
    function getTotalResults() public view returns (uint256) {
        return results.length;
    }
}