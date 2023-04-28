// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface VideoProcessing {
    function getProcessedVideos(uint startIndex, uint numElements) external view returns (VideoProcessing.Video[] memory);
    function getVideo(uint index) external view returns (Video memory);
    function getVideoOwner(uint index) external view returns (address payable);
    function getSwearCount(uint index) external view returns (uint);
    function getSafetyScore(uint index) external view returns (uint);
    function getLanguages(uint index) external view returns (string[] memory);
    function getTopicKeys(uint index) external view returns (string[] memory);
    function getTopicValues(uint index) external view returns (string[] memory);

    struct Video {
        address owner;
        string player_uri;
        string playback_uri;
        uint swear_count;
        string[] topicKeys;
        string[] topicValues;
        uint safety_score;
        string[] languages;
    }
}

contract VideoDonation {
    function donate(address videoProcessing, uint maxTries, uint maxSwearCount, uint minSafetyScore, string memory language,
    string[] memory topics, string[] memory sentiments) public payable{
        require(topics.length == sentiments.length, "Topics and Sentiments must have same length");
        VideoProcessing videos = VideoProcessing(videoProcessing);
        for (uint i = 0; i < maxTries; i++) {
            VideoProcessing.Video memory video = videos.getVideo(i);
            if (_matchesCriteria(video, maxSwearCount, minSafetyScore, language, topics, sentiments)) {
                address payable owner = videos.getVideoOwner(i);
                uint amount = msg.value;
                (bool success, ) = owner.call{value: amount}("");
                require(success, "Failed to send ether to owner");
                break;
            }
        }
    }

    function _matchesCriteria(VideoProcessing.Video memory video, uint maxSwearCount, uint minSafetyScore, string memory language,
    string[] memory topics, string[] memory sentiments) public pure returns(bool){
        if (video.swear_count > maxSwearCount || video.safety_score < minSafetyScore) {
            return false;
        }

        bool has_language = false;
        for (uint i = 0; i < video.languages.length; i++) {
            if (keccak256(abi.encodePacked((video.languages[i]))) == keccak256(abi.encodePacked((language)))) {
                has_language = true;
            }
        }

        if (!has_language) {
            return false;
        }
        
        bool has_key_values = true;
        for (uint i = 0; i < topics.length; i++) {
            bool found = false;
            for (uint j = 0; j < video.topicKeys.length; j++) {
                if (keccak256(abi.encodePacked((topics[i]))) == keccak256(abi.encodePacked((video.topicKeys[j])))) {
                    if (keccak256(abi.encodePacked((sentiments[i]))) != keccak256(abi.encodePacked((video.topicValues[j])))) {
                        has_key_values = false;
                    }
                    found = true;
                }
            }
            if (!found) {
                has_key_values = false;
            }
        }

        if (!has_key_values) {
            return false;
        }

        return true;
    }
}