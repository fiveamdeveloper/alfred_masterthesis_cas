import ChatInput from "./ChatInput/ChatInput";
import MessageList from "./MessageList/MessageList";
<<<<<<< Updated upstream

function ChatWindow() {
    return (
        <div className='col d-flex flex-column' style={{ height: '100%' }}>
            <div className="flex-grow-1 overflow-auto">
                < MessageList />
            </div>
            <ChatInput />
        </div >

import { Alert, Button } from "react-bootstrap";
import { useState, useEffect, useRef } from 'react';
import Image from "react-bootstrap/Image";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row"
import { Card } from "react-bootstrap";
import { PlayFill } from "react-bootstrap-icons";

import logo from "./logo_alfred.png";
import "./ChatWindow.css";

function ChatWindow() {
    const [messages, setMessages] = useState([]); // Zustand für Nachrichten
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState('')
    const [hasScrollbar, setHasScrollbar] = useState(false);
    const historyRef = useRef(null);
    const messagesEndRef = useRef(null);

    const checkForScrollbar = () => {
        const element = historyRef.current;
        if (element) {
            const scrollbarPresent = element.scrollHeight > element.clientHeight;
            setHasScrollbar(scrollbarPresent);
        }
    };

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    useEffect(() => {
        checkForScrollbar();
        window.addEventListener('resize', checkForScrollbar);
        //console.log("Resize triggered...")
        // Clean-up-Funktion
        return () => window.removeEventListener('resize', checkForScrollbar);
    }, []);

    let names = ["James", "Lisa", "John", "Jessica", "Tyler", "Scott", "Paula", "Mackenzie"]

    let namesLength = names.length;
    let randomIndex = Math.floor(Math.random() * namesLength);

    let randomName = names[randomIndex];

    return (
        <Col className='d-flex flex-column justify-content-between h-100 m-0' style={{ height: '100vh' }}>
            {
                messages.length === 0 ?
                    <Row className="flex-grow-1">
                        <Col className="w-100 d-flex flex-column justify-content-center align-items-center" xs={6} md={4}>
                            <Image className="shadow" src={logo} style={{ width: '200px', height: '200px' }} roundedCircle />
                            <h5 className="my-3 text-center">Hi, {randomName}!</h5>
                            <h6>Was kann ich heute für dich tun?</h6>
                        </Col>
                    </Row> : null
            }

            {
                messages.length !== 0 ? < div className={`flex-grow-1 overflow-auto ${hasScrollbar ? "scrollbar-pr" : ""}`} ref={historyRef} >
                    <MessageList messages={messages} />
                    <div ref={messagesEndRef} />
                </div > : null
            }

            {/*error ? <Alert variant="danger" className="mt-3">
                Es ist ein Fehler aufgetreten. Bitte versuche es erneut.
        </Alert> : ""*/}

            {
                messages.length === 0 ?
                    <div className="d-flex flex-column flex-sm-row">
                        <Col lg={4} md={6} className="d-flex flex-md-grow-1 flex-grow-0 flex-column justify-content-end pb-3">
                            <Card className="me-sm-2">
                                <Card.Body className="d-flex flex-row justify-content-between">
                                    <div>
                                        <Card.Subtitle className="mb-2 text-muted">Überprüfe den Status</Card.Subtitle>
                                        <Card.Text>
                                            eines Fertigungsauftrages
                                        </Card.Text>
                                    </div>
                                    <div className="d-flex flex-fill justify-content-end">
                                        <Button variant="outline-primary"><PlayFill /></Button>
                                    </div>
                                </Card.Body>
                            </Card>
                        </Col>
                        <Col lg={4} md={6} className="d-flex flex-md-grow-1 flex-grow-0 flex-column justify-content-end pb-3">
                            <Card className="ms-sm-2 me-sm-2">
                                <Card.Body className="d-flex flex-row justify-content-between">
                                    <div >
                                        <Card.Subtitle className="mb-2 text-muted">Gib einen Fertigungsauftrag</Card.Subtitle>
                                        <Card.Text>
                                            frei oder schließe ihn technisch ab
                                        </Card.Text>
                                    </div>
                                    <div className="d-flex flex-fill justify-content-end">
                                        <Button variant="outline-primary"><PlayFill /></Button>
                                    </div>
                                </Card.Body>
                            </Card>
                        </Col>
                        <Col lg={4} className="d-flex flex-md-grow-1 flex-grow-0 d-none d-lg-block flex-column justify-content-end pb-3">
                            <Card className="ms-sm-2">
                                <Card.Body className="d-flex flex-row justify-content-between">
                                    <div >
                                        <Card.Subtitle className="mb-2 text-muted">Lass dir die Komponenten</Card.Subtitle>
                                        <Card.Text>
                                            zu einem Fertigungsauftrag anzeigen
                                        </Card.Text>
                                    </div>
                                    <div className="d-flex flex-fill justify-content-end">
                                        <Button variant="outline-primary"><PlayFill /></Button>
                                    </div>
                                </Card.Body>
                            </Card>
                        </Col>
                    </div> : null
            }

            <ChatInput setMessages={setMessages} messages={messages} setIsLoading={setIsLoading} isLoading={isLoading} setError={setError} />


        </Col>
    );
}

export default ChatWindow;
