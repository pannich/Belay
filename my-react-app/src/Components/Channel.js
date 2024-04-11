import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { MessagesContainer } from './Messages';
import { useNavigate, useParams } from 'react-router-dom';
import { ReplyMessages } from './ReplyMessages';
import "./Channel.css";

var USERTOKEN = '';
var USER_ID = '';
var config = {};

export const markMessagesAsRead = async (channelId) => {
  var latestMessage = '';
  try { // Fetch latest message
    const response  = await axios.get(`/api/messages?channel_id=${channelId}`, config);
    if (response.data.length > 0) {
        latestMessage = response.data[response.data.length - 1];  // Get the latest message
        console.log(`Channel Latest Message${latestMessage}`);
    } else {
        console.log('No messages found');
    }
  } catch (error) {
    console.error('Error fetching the latest message:', error);
  }

  // Mark messages as read when visiting a channel
  const last_message_id_seen = latestMessage.id;
  const user_id = Number(USER_ID);

  try {
    const response = await axios.post(`/api/channels/${channelId}/updateLastSeen`, {"channel_id": channelId, "user_id": user_id, "last_message_id_seen": last_message_id_seen}, config);
  } catch (error) {
    console.error('Failed to fetch messages:', error);
  }

  // Optionally, refetch channels or update state to reflect the new unread count
};

function CreateChannel({onChannelCreated}) {
  const [input, setInput] = useState("");
  // api to create new channel
  console.log(`create channel`);
  const createChannel = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/channels', {'name': input} , config);
      setInput("");     // clear input
      if (onChannelCreated) onChannelCreated(input); // Callback for parent component
      return response.data;
    } catch (error) {
      console.error('Failed to fetch messages:', error);
    }
    return;
  };

  return (
    <div className="createChannel">
      <form onSubmit={createChannel}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={`Enter Channel Name}`}
        />
        <button type="submit">CREATE</button>
      </form>
    </div>
  );
};

const ChannelsList = () => {
  const [visibleComponent, setVisibleComponent] = useState('channels'); // Possible values: 'channels', 'messages', 'replies'
  const [channels, setChannels] = useState([]);
  const [newChannel, setnewChannel] = useState(false);
  const [currentChannelId, setCurrentChannelId] = useState(null);
  const [showReplies, setShowReplies] = useState(false);
  const [repliesToMsg, setRepliesToMsg] = useState('');
  const navigate = useNavigate();
  const { channelId } = useParams();
  USER_ID = localStorage.getItem('nichada_userId');
  USERTOKEN = localStorage.getItem('nichada_belay_auth_key');
  config = {
    headers: {
      'Content-Type': 'application/json', // Specify the content type
      'Authorization': `${USERTOKEN}` // Authorization header, for example, a Bearer token
    }
  };

  //-------- Channel ---------

  // Fetch channels and unread counts
  useEffect(() => {
    async function fetchChannelUnreadCounts() {  // uniquely for this user. Identify user by token in the header
      try {
          const response = await axios.get('/api/messages/unread_counts', config);
          console.log(`Fetch unread count`);
          console.log(response.data);
          setChannels(response.data); // Directly set the fetched data to your state
          setnewChannel(false);
      } catch (error) {
          console.error('Failed to fetch unread counts:', error);
      }
    }
    fetchChannelUnreadCounts(); // Immediately fetch unread counts when page load

    // Set up an interval to channel every 1 sec
    const intervalId = setInterval(() => {    // intervalId holds the reference ID returned by setInterval().
      console.log('Checking for unread messages');
      fetchChannelUnreadCounts(); // Fetch new messages
    }, 1000);

    // Cleanup function to clear the interval
    return () => clearInterval(intervalId);
  }, [newChannel]); // The empty array means this effect runs once after the initial render and return when unmount i.e. navigate to different page or page refresh.

  const handleChannelClick = (channelId) => {
    setCurrentChannelId(channelId);
    setVisibleComponent('messages');
    markMessagesAsRead(channelId);
    navigate(`/channel/${channelId}`);
  };

  const getChannelNameById = (channelId) => {
    // console.log(`Channel ID: ${typeof channelId}`);
    const channel = channels.find(channel => channel.id === Number(channelId));
    return channel ? channel.name : undefined;
  }

  const handleChannelCreated = (channelName) => {
    setnewChannel(true);
    console.log(`Channel created: ${channelName}`);
  };

  //-------- Narrow Screen ---------
  // This effect updates visibleComponent when showReplies changes.
  useEffect(() => {
    if (showReplies) {
      setVisibleComponent('replies'); // Show replies if showReplies is true
    } else {
      setVisibleComponent('messages'); // Show messages if showReplies is false
    }
  }, [showReplies]); // This effect depends on showReplies

  useEffect(() => {
    if (!channelId) {
      setVisibleComponent('channels'); // Show replies if showReplies is true
    }
  }, [channelId]); // This effect depends on showReplies

  //----------------------------------

  return (
    <div className="app-container">
      {/* sidebar */}
      <div className={`sidebar-container ${visibleComponent === 'channels' ? 'active-component' : ''}`}>
        <h2>Channels</h2>
        <ul>
        {channels.length > 0 ? (channels.map(channel => (
          <li key={channel.id}
          className = {`channel ${currentChannelId === channel.id ? 'current-channel' : ''}`}
          onClick={() => handleChannelClick(channel.id)
          }>
            {channel.name} - Unread messages: {channel.unread_count}
          </li>
          ))
        ) : (
          <p>No channel available.</p> // Placeholder or any other content for empty state
        )
        }
        <CreateChannel onChannelCreated={handleChannelCreated} />
        </ul>
        </div>

      {/* chat */}
      <div className={`chat-message-container ${visibleComponent === 'messages' ? 'active-component' : ''}`}>
        <MessagesContainer
        channelId={channelId}
        channelName={getChannelNameById(channelId)}
        setShowReplies={setShowReplies}
        setRepliesToMsg={setRepliesToMsg}/>
      </div>

      {/* reply thread */}
      {showReplies && (
        <div className={`reply-message-container ${visibleComponent === 'replies' ? 'active-component' : ''}`}>
          Reply messages...
          <button className='closeBtn' onClick={() => setShowReplies(false)}> Close </button>
          <ReplyMessages channelId={channelId} channelName={getChannelNameById(channelId)} messageId={repliesToMsg}/>
          {/* Reply messages */}
        </div>
      )}
    </div>
  );
}

export default ChannelsList;

// ----------------------------------------------------------------------------
