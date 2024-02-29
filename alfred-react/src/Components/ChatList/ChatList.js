import { Card, ListGroup } from "react-bootstrap";
import ChatListItem from "./ChatListItem/ChatListItem";

function ChatList() {
    let topics = [
        { "topic": "Fertigungsauftrag 4711" },
        { "topic": "Rückmeldung 49" }
    ]

    return (
        <div className='col-3 d-none d-lg-block'>
            <Card className="my-3">
                <ListGroup variant="flush">
                    {
                        topics.map((topic, index) => (
                            <ListGroup.Item key={index}><ChatListItem key={index} topic={topic} /></ListGroup.Item>
                        ))
                    }
                </ListGroup>
            </Card>
        </div>

    );
}

export default ChatList;
