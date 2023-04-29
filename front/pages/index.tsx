import Image from 'next/image'
import { Inter } from 'next/font/google'
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { Children, useEffect, useState, useCallback } from 'react';



export const getCookiesAsObject = () => {
  // stolen: https://stackoverflow.com/a/64472572
  return Object.fromEntries(
    document.cookie
      .split('; ')
      .map(v => v.split(/=(.*)/s).map(decodeURIComponent)),
  );
};

export const getServerSideProps = async ({req} : {req: any}) => {
  if (req.method == "POST") {
    const streamPromise = new Promise( ( resolve, reject ) => {
        let body = ''
        req.on('data', (chunk : any) => {
          body += chunk
        })
        req.on('end', () => {
          console.log(body);
          resolve(body)
        });
    } );
    const res = await streamPromise;
    if (typeof res !== "string") throw new Error("Not a string")
    return { props: { data: JSON.parse(res) } };
  }
  return { props: {} };
};

export default function Index({ state, updateTheme }): JSX.Element {
  //hello alter
  console.log("STATE", state);
  
  const [socketUrl, setSocketUrl] = useState(process.env.NEXT_PUBLIC_WS_PATH);
  const [messageHistory, setMessageHistory] = useState([]);
  const [onlineChatId, setOnlineChatId] = useState(0);

  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);

  useEffect(() => {
    if (lastMessage !== null) {
      setMessageHistory((prev) => prev.concat(lastMessage));
      const data = JSON.parse(lastMessage.data);
      console.log("message receiveed", data);
      /**
       * Here we can process any incoming websocket calls
       */
    }
  }, [lastMessage, setMessageHistory]);

  
  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Connected',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Offline',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState];

  return (<h1>
    <button className="btn">Hello daisyUI</button>
    <button className="btn">{connectionStatus}</button>
    <input type="text" placeholder="Type here" className="input w-full max-w-xs" />
    <button className="btn" onClick={() => {
          sendMessage(
            JSON.stringify({
              type: 'new_message',
              text: '@ai how are you?',
              project_hash: 'f8f65557-e7dc-43c5-bcf1-3bd557c2d324',
              data: {}
            })
          );
    }}>Send test message</button>
    </h1>);
}
