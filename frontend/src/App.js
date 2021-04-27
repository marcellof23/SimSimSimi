import {useState,useEffect} from 'react'
import BotSide from './components/BotSide'
import ClientSide from "./components/ClientSide";
import Messages from "./components/Messages";
import Input from "./components/Input";
import Header from "./components/Header";
import "./style.css";
import "./chatbot.scss"
import API from "./API";
import {BrowserRouter as Router, Route} from 'react-router-dom'
const App = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    async function loadWelcomeMessage() {
      setMessages([
        <BotSide
          key="0"
          fetchMessage={async () => await API.GetChatbotResponse("hi")}
        />
      ]);
    }
    loadWelcomeMessage();
  }, []);

  const send = async text => {
    const newMessages = messages.concat(
      <ClientSide key={messages.length + 1} text={text} />,
      <BotSide
        key={messages.length + 2}
        fetchMessage={async () => await API.GetChatbotResponse(text)}
      />
    );
    setMessages(newMessages);
  };

  return (
    <div className="chatbot">
      <Header />
      <Messages messages={messages} />
      <Input onSend={send} />
    </div>
  );
}

export default App;
