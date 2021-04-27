import React from "react";

export default function ClienSide({ text }) {
  return (
    <div className="message-container">
      <div className="user-message">{text}</div>
    </div>
  );
}
