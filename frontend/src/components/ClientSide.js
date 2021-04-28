import React from "react";
import Avatar from 'react-avatar';

export default function ClienSide({ text }) {
  return (
    <div className="message-container-client">
      <span className="user-message">{text}</span>
      <span><Avatar githubHandle="weebs" size={50} round="20px" /></span>
    </div>
  );
}
