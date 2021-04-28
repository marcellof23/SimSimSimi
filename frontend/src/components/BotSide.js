import React, { useState, useEffect } from "react";
import Avatar from 'react-avatar';

export default function BotMessage({ fetchMessage }) {
  const [isLoading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  var audio = new Audio("/Blop.mp3");
  audio.volume = 0.4;
  useEffect(() => {
    async function loadMessage() {
      const msg = await fetchMessage();
      setLoading(false);
      setMessage(msg);
      audio.play();
    }
    loadMessage();
  }, [fetchMessage]);

  return (
    <div className="message-container-bot">
      <div><Avatar githubHandle="weebs" size={50} round="20px" /></div>
      <div className="bot-message">{isLoading ? "..." : message}</div>
    </div>
  );
}
