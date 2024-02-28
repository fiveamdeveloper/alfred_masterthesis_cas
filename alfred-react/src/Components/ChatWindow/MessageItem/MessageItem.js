//import { CardText } from 'react-bootstrap';
import Card from 'react-bootstrap/Card';

function MessageItem({ message }) {
    console.log("message:", message)

    return (
<<<<<<< Updated upstream
        <div className={`d-flex ${message.role === "user" ? "justify-content-start" : "justify-content-end"} my-3`}>
            <Card className='w-75'>
                <Card.Body>
                    <Card.Subtitle className="mb-2 text-muted">{message.role}</Card.Subtitle>
                    <CardText>
                        <div>{message.response}</div>
                    </CardText>
=======
        <div className={`d-flex ${message.role === "user" ? "justify-content-start" : "justify-content-end"} my-3 message-item`}>
            <Card border={message.type === "danger" ? "danger" : " "} className='w-75'>
                <Card.Body>
                    <Card.Subtitle className="mb-2 text-muted">{message.role === "user" ? "Felix" : "Alfred"}</Card.Subtitle>

                    <div dangerouslySetInnerHTML={{ __html: message.content }} />

                    <ReactMarkdown>
                        {/*message.content*/}
                    </ReactMarkdown>
>>>>>>> Stashed changes
                </Card.Body>
            </Card>
        </div >
    );
}

export default MessageItem;
