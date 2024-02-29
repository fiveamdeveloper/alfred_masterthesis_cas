import Card from 'react-bootstrap/Card';
import ReactMarkdown from 'react-markdown';

import "./MessageItem.css";

function MessageItem({ message }) {
    console.log("message:", message)

    return (
        <div className={`d-flex ${message.role === "user" ? "justify-content-start" : "justify-content-end"} my-3 message-item`}>
            <Card border={message.type === "danger" ? "danger" : " "} className='w-75'>
                <Card.Body>
                    <Card.Subtitle className="mb-2 text-muted">{message.role === "user" ? "Felix" : "Alfred"}</Card.Subtitle>

                    <ReactMarkdown>
                        {String(message.content)}
                    </ReactMarkdown>
                </Card.Body>
            </Card>
        </div>
    );
}

export default MessageItem;
