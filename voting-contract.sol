
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PreferentialVoting {
    address public electionAuthority;
    uint public registerByDeadline;
    uint public voteByDeadline;
    uint public revealVoteByDeadline;
    uint public votingTax;
    uint public totalTaxCollected;

    struct Candidate {
        string name;
        uint voteCount;
    }

    struct Voter {
        bool registered;
        bool voted;
        bool revealed;
        uint[] vote;
        uint taxPaid;
    }

    mapping(address => Voter) public voters;
    Candidate[] public candidates;

    modifier onlyElectionAuthority() {
        require(msg.sender == electionAuthority, "Only election authority can call this function");
        _;
    }

    constructor() {
        electionAuthority = msg.sender;
    }

    function setRegisterByDeadline(uint _deadline) public onlyElectionAuthority {
        registerByDeadline = _deadline;
    }

    function setVoteByDeadline(uint _deadline) public onlyElectionAuthority {
        require(_deadline > registerByDeadline, "Vote by deadline must be after register by deadline");
        voteByDeadline = _deadline;
    }

    function setRevealVoteByDeadline(uint _deadline) public onlyElectionAuthority {
        require(_deadline > voteByDeadline, "Reveal vote by deadline must be after vote by deadline");
        revealVoteByDeadline = _deadline;
    }

    function setVotingTax(uint _amount) public onlyElectionAuthority {
        require(block.timestamp < registerByDeadline, "Cannot change voting tax after register by deadline");
        votingTax = _amount;
    }

    function registerVoter(address _voter) public onlyElectionAuthority {
        require(!voters[_voter].registered, "Voter already registered");
        voters[_voter].registered = true;
    }

    function registerCandidate(string memory _name) public onlyElectionAuthority {
        candidates.push(Candidate(_name, 0));
    }

    function blindedVote(uint[] memory _data) public payable {
        require(block.timestamp >= registerByDeadline && block.timestamp < voteByDeadline, "Voting not permitted now");
        require(voters[msg.sender].registered, "Voter not registered");
        require(!voters[msg.sender].voted, "Voter already voted");

        require(msg.value >= votingTax, "Insufficient voting tax");
        uint refundAmount = msg.value - votingTax;
        if (refundAmount > 0) {
            payable(msg.sender).transfer(refundAmount);
        }

        voters[msg.sender].vote = _data;
        voters[msg.sender].voted = true;
        voters[msg.sender].taxPaid = votingTax;
        totalTaxCollected += votingTax;
    }

    function unblindVote(uint[] memory _vote) public {
        require(block.timestamp >= voteByDeadline && block.timestamp < revealVoteByDeadline, "Vote revealing not permitted now");
        require(voters[msg.sender].registered, "Voter not registered");
        require(voters[msg.sender].voted, "Voter has not voted yet");
        require(!voters[msg.sender].revealed, "Vote already revealed");

        require(isValidVote(_vote), "Invalid vote");

        voters[msg.sender].vote = _vote;
        voters[msg.sender].revealed = true;
    }

    function isValidVote(uint[] memory _vote) internal view returns (bool) {
        if (_vote.length != candidates.length) {
            return false;
        }
        bool[] memory found = new bool[](candidates.length);
        for (uint i = 0; i < _vote.length; i++) {
            if (_vote[i] < 1 || _vote[i] > candidates.length || found[_vote[i] - 1]) {
                return false;
            }
            found[_vote[i] - 1] = true;
        }
        return true;
    }

    function countVotes() internal {
        
    }

    function winner() public view returns (uint) {
        
    }
}
