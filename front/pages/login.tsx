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
  
  const [loginData, setLoginData] = useState({
    username:'',
    password:''
  })
  
  const loginRequest = () => {
    fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify(loginData)
    }).then((res) => {
      res.json().then((data) => {
        console.log(data);
      })
    })
  }
  //hello alter
  return (<div>
      <button className="btn">
        This is a trashy placeholder for a real login api
      </button>
      <input type="text" placeholder="username" onChange={(e) => {setLoginData({...loginData, username: e.target.value})}} className="input input-bordered input-sm w-full max-w-xs" />
      <input type="text" placeholder="password" onChange={(e) => {setLoginData({...loginData, password: e.target.value})}} className="input input-bordered input-sm w-full max-w-xs" />
    </div>);
}
