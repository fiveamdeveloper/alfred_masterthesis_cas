<<<<<<< Updated upstream
import { FormControl, Button, Form } from 'react-bootstrap';
=======
import { FormControl, Button, Form, Spinner } from 'react-bootstrap';
import { useState } from 'react';
import { SendFill } from 'react-bootstrap-icons';
import { Alert } from 'react-bootstrap';

function ChatInput({ messages, setMessages, setIsLoading, isLoading, setError, error }) {
    const [inputValue, setInputValue] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault()

        if (inputValue !== "") {

            setMessages(prevMessages => [...prevMessages, {
                "role": "user",
                "content": inputValue
            }]);

            setIsLoading(true)
            setError("")

            // Sendet die Benutzereingabe an das Backend
            fetch(`http://localhost:3005/api/v1/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ "content": inputValue }),
            }).then(response => {
                if (!response.ok) {
                    setError(response.status)
                    throw new Error('Netzwerk-Antwort war nicht ok');
                }
                setError()
                return response.json(); // Verarbeitet die Antwort als JSON
            })
                .then(data => {
                    console.log(data)
                    // Setzt die Antwort des Assistenten

                    // Fügt die Benutzernachricht zum Zustand hinzu
                    setMessages(prevMessages => [...prevMessages, {
                        "role": "assistant",
                        "content": data.content,
                        "type": data.type
                    }]);
                    setIsLoading(false)
                })
                .catch(error => {
                    setIsLoading(false)
                    console.error('Fetch-Fehler:', error);
                    setMessages(prevMessages => [...prevMessages, {
                        "role": "assistant",
                        "content": error,
                        "type": "danger"
                    }]);
                });

            setInputValue(""); // Setzt das Eingabefeld zurück
            let resetRows = (event) => {
                event.target.style.height = "auto"
            }

            resetRows(event)
        }
    };

    const handleChange = (event) => {
        setInputValue(event.target.value);
        adjustHeight(event); // Füge dies hinzu, um die Höhe anzupassen
    };

    // Funktion, um die Höhe der Textarea automatisch anzupassen
    const adjustHeight = (event) => {
        event.target.style.height = 'auto';
        event.target.style.height = `${event.target.scrollHeight}px`;
    };

    const handleKeyDown = (event) => {
        // Prüfen, ob Enter gedrückt wurde und nicht die Shift-Taste gehalten wird
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Verhindern, dass ein Zeilenumbruch eingefügt wird
            handleSubmit(event); // Formular absenden
        }
    };
>>>>>>> Stashed changes

function ChatInput() {
    return (
<<<<<<< Updated upstream
        <Form className="d-flex mb-3">
            <FormControl type="text" placeholder="Nachricht eingeben..." className="me-2" />
            <Button variant="primary" type="submit">Senden</Button>
        </Form>
=======
        <Form className="d-flex mb-5 mb-sm-3" onSubmit={handleSubmit}>
            <FormControl as="textarea" rows={1} placeholder={/*isLoading ? "The magic happens now..." : */"Nachricht eingeben..."} className="me-2" value={inputValue} onChange={handleChange} onKeyDown={handleKeyDown}
                name="messageInput" autoComplete='off' style={{
                    overflow: 'hidden',
                    resize: 'none',
                }} spellCheck="false" />
            <Button className="align-self-end col-sm-2 col-2" variant="primary" type="submit" disabled={isLoading}>{isLoading ? <Spinner
                animation="border"
                size="sm" /> : <SendFill />}</Button>
        </Form >

>>>>>>> Stashed changes
    );
}

export default ChatInput;
