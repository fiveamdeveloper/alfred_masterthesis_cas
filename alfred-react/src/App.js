import './App.css';
import ChatList from './Components/ChatList/ChatList';
import ChatWindow from './Components/ChatWindow/ChatWindow';
import { Row } from 'react-bootstrap';
import { Container } from 'react-bootstrap';
import { useEffect } from 'react';

//import Card from 'react-bootstrap/Card';
//import ListGroup from 'react-bootstrap/ListGroup';
import Header from './Components/Header/Header';


function App() {

  useEffect(() => {
    document.title = "Alfred";
  }, []);

  return (
    <Container className='bg-light' fluid>
      <Header />

      <Row>
        {/*<ChatList />*/}
        <ChatWindow />
      </Row>
    </Container>
  );
}

export default App;
