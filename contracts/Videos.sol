// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract VideoProcessing {
    struct Video {
        address payable owner;
        string player_uri;
        string playback_uri;
        uint swear_count;
        string[] topicKeys;
        string[] topicValues;
        uint safety_score;
        string[] languages;
    }

    Video[] public processed_videos;

    function addVideo(
        address payable _owner,
        string memory _player_uri,
        string memory _playback_uri,
        uint _swear_count,
        string[] memory _topicKeys,
        string[] memory _topicValues,
        uint _safety_score,
        string[] memory _languages
    ) public {
        require(_topicKeys.length == _topicValues.length, "Keys and Values must have same length");

        // Create dynamic arrays for the topics and languages
        string[] memory topicKeys = new string[](_topicKeys.length);
        string[] memory topicValues = new string[](_topicValues.length);
        string[] memory languages = new string[](_languages.length);

        // Copy the topic keys and values to their respective arrays
        for (uint i = 0; i < _topicKeys.length; i++) {
            topicKeys[i] = _topicKeys[i];
            topicValues[i] = _topicValues[i];
        }

        // Copy the languages to the languages array
        for (uint i = 0; i < _languages.length; i++) {
            languages[i] = _languages[i];
        }

        // Create a new video object and add it to the processed_videos array
        Video memory newVideo = Video({
            owner: _owner,
            player_uri: _player_uri,
            playback_uri: _playback_uri,
            swear_count: _swear_count,
            topicKeys: topicKeys,
            topicValues: topicValues,
            safety_score: _safety_score,
            languages: languages
        });

        processed_videos.push(newVideo);
    }

    function getProcessedVideos(uint startIndex, uint numElements) public view returns (Video[] memory) {
        require(startIndex < processed_videos.length, "Start index is out of range");
        uint endIndex = startIndex + numElements;
        if (endIndex > processed_videos.length) {
            endIndex = processed_videos.length;
        }
        uint resultLength = endIndex - startIndex;
        Video[] memory result = new Video[](resultLength);
        for (uint i = 0; i < resultLength; i++) {
            result[i] = processed_videos[startIndex + i];
        }
        return result;
    }

    function getVideo(uint index) public view returns (Video memory) {
        return processed_videos[index];
    }

    function getVideoOwner(uint index) public view returns (address payable) {
        return processed_videos[index].owner;
    }

    function getPlayerUri(uint index) public view returns (string memory) {
        return processed_videos[index].player_uri;
    }

    function getPlaybackUri(uint index) public view returns (string memory) {
        return processed_videos[index].playback_uri;
    }

    function getSwearCount(uint index) public view returns (uint) {
        return processed_videos[index].swear_count;
    }

    function getTopicKeys(uint index) public view returns (string[] memory) {
        return processed_videos[index].topicKeys;
    }

    function getTopicValues(uint index) public view returns (string[] memory) {
        return processed_videos[index].topicValues;
    }

    function getSafetyScore(uint index) public view returns (uint) {
        return processed_videos[index].safety_score;
    }

    function getLanguages(uint index) public view returns (string[] memory) {
        return processed_videos[index].languages;
    }

    receive() external payable {
        address payable owner = payable(msg.sender);
        uint amount = msg.value;
        owner.transfer(amount);
    }
    
    function getBalance() external view returns(uint) {
        return address(this).balance;
    }

    function getBalanceOf(address video_owner) external view returns(uint) {
        return video_owner.balance;
    }
}