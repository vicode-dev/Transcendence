// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GameResults {
    struct GameResult {
        uint64 gameId;
        uint32[] playerIds;
        uint8[] score;
        bool gameType;
        uint64 startTime;
        uint64 endTime;
    }

    struct Tournament {
        uint32 tournamentId;
        uint64[] gameIds;
        uint32[] playerIds;
    }

    // Store game results
    GameResult[] public results;
    Tournament[] public tournament;
    address author;
    
    constructor() {
        author = msg.sender;
    }

    // Event to log the addition of a new game result
    event GameAdded(uint64 gameId);

    event TournamentAdded(uint32 tournamentId);

    function addGame(uint32[] memory _playerIds, uint8[] memory _score, bool _gameType, uint64 _startTime, uint64 _endTime) public {
        require(author == msg.sender, "Not authorized to add a game");
        GameResult memory newResult = GameResult({
            gameId: uint64(results.length),
            playerIds: _playerIds,
            score: _score,
            gameType: _gameType,
            startTime: _startTime,
            endTime: _endTime
        });

        results.push(newResult);
        emit GameAdded(newResult.gameId);
    }

    function getGameById(uint64 index) public view returns (GameResult memory) {
        require(index < results.length, "Game result does not exist");
        return (results[index]);
    }

    function getGamesByPlayer(uint32 index) public view returns (GameResult[] memory) {
        uint64 count = 0;
        for (uint32 i = 0; i < results.length; i++) {
            for (uint32 j = 0; j < results[i].playerIds.length; j++)
            {
                if(index == results[i].playerIds[j])
                    count++;
            }
        }
        GameResult[] memory games = new GameResult[](count);
        for (uint32 i = 0; i < results.length; i++) {
            for (uint32 j = 0; j < results[i].playerIds.length; j++)
            {
                if(index == results[i].playerIds[j])
                    games[--count] = results[i];
            }
        }
        return games;
    }

    function getGamesNumber() public view returns (uint256) {
        return results.length;
    }

    function addTournament(uint64[] memory _gameIds, uint32[] memory _playerIds) public
    {
        require(author == msg.sender, "Not authorized to add a game");
        Tournament memory newResult = Tournament({
            tournamentId: uint32(tournament.length),
            gameIds: _gameIds,
            playerIds: _playerIds
        });
        tournament.push(newResult);

        emit TournamentAdded(newResult.tournamentId);
    }

    function getTournamentById(uint32 index) public view returns (Tournament memory) {
        require (index < tournament.length, "Tournament does not exist");
        return (tournament[index]);
    }

    function getAllTournaments() public view returns (Tournament[] memory) {
        return tournament;
    }

    function getTournamentByPlayer(uint32 index) public view returns (Tournament[] memory) {
        uint32 count = 0;
        for (uint32 i = 0; i < tournament.length; i++) {
            for (uint32 j = 0; j < tournament[i].playerIds.length; j++)
            {
                if(index == tournament[i].playerIds[j])
                {
                    count++;
                    break;
                }
                    
            }
        }
        Tournament[] memory tournaments = new Tournament[](count);
        for (uint32 i = 0; i < tournament.length; i++) {
            for (uint32 j = 0; j < tournament[i].playerIds.length; j++)
            {
                if(index == tournament[i].playerIds[j])
                {
                    tournaments[--count] = tournament[i];
                    break;
                }
            }
        }
        return tournaments;
    }

}