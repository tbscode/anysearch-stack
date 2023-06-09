import Image from "next/image";
import { Inter } from "next/font/google";
import { useEffect, useRef, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";

function getFileExtensionFromBase64(base64String) {
  const fileExtensionRegex = /^data:[a-zA-Z]+\/([a-zA-Z0-9-.+]+);/;

  const match = base64String.match(fileExtensionRegex);
  if (match && match[1]) {
    return match[1];
  }

  return 'unknown';
}

function downloadBase64File(base64String, fileName) {
  const link = document.createElement('a');
  link.href = base64String;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function getFileTypeFromBase64(base64String) {
  const fileTypeRegex = /^data:([a-zA-Z]+\/[a-zA-Z0-9-.+]+);/;

  const match = base64String.match(fileTypeRegex);
  if (match && match[1]) {
    const fileType = match[1].split('/')[0];
    return fileType;
  }

  return 'unknown';
}
import { Flag } from 'react-world-flags';

export const getCookiesAsObject = () => {
  // stolen: https://stackoverflow.com/a/64472572
  return Object.fromEntries(
    document.cookie
      .split("; ")
      .map((v) => v.split(/=(.*)/s).map(decodeURIComponent))
  );
};

function FlagComponent({ country }) {
  // Convert the country name to the ISO 3166-1 alpha-2 code
  const countryCodes = {
    serbian: 'RS',
    // Add more country codes here
  };
  const countryCode = countryCodes[country.toLowerCase()];

  // return <Flag code={countryCode} />;
}


function isBase64Image(base64String) {
  const imageFormatRegex = /^data:image\/[a-zA-Z]+;base64,/;

  return imageFormatRegex.test(base64String);
}

function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      let encoded = reader.result.toString()
      if ((encoded.length % 4) > 0) {
        encoded += '='.repeat(4 - (encoded.length % 4));
      }
      resolve(encoded);
    };
    reader.onerror = error => reject(error);
  });
}

export const getServerSideProps = async ({ req }: { req: any }) => {
  if (req.method == "POST") {
    const streamPromise = new Promise((resolve, reject) => {
      let body = "";
      req.on("data", (chunk: any) => {
        body += chunk;
      });
      req.on("end", () => {
        console.log(body);
        resolve(body);
      });
    });
    const res = await streamPromise;
    if (typeof res !== "string") throw new Error("Not a string");
    return { props: { data: JSON.parse(res) } };
  }
  return { props: {} };
};

export default function Chat({ state, setState, updateTheme }): JSX.Element {
  console.log("STATE", state);
  const scrollRef = useRef(null);
  const fileInputRef = useRef(null);
  const [isHomeClicked, setIsHomeClicked] = useState(false);

  const navStyle = isHomeClicked ? { display: 'flex' } : { display: 'none' };

  function handleHomeClick() {
    setIsHomeClicked(!isHomeClicked);
  }

  const [inputValue, setInputValue] = useState("");

  function handleInputChange(event) {
    setInputValue(event.target.value);
  }

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [scrollRef.current]);

      
      function handleClick() {
        fileInputRef.current.click();
      }

  console.log("DATA", state.data);

  console.log("STATE", state);

  const [socketUrl, setSocketUrl] = useState(process.env.NEXT_PUBLIC_WS_PATH);
  const [messageHistory, setMessageHistory] = useState([]);
  const [onlineChatId, setOnlineChatId] = useState(0);
  const [inputState, setInputState] = useState("");
  const [curProject, setCurProject] = useState(0);
  const [selectedLanguage, setSelectedLanguage] = useState(
    !state.data ? "english" : state.data.language
  );

  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }

    if (lastMessage !== null) {
      setMessageHistory((prev) => prev.concat(lastMessage));
      const data = JSON.parse(lastMessage.data);
      console.log("message receiveed", data);
      /**
       * Here we can process any incoming websocket calls
       */
      if (data.event === "new_message") {
        const newState = JSON.parse(JSON.stringify(state));

        // TODO don't use current project but deteermine it by project hash!
        console.log("OWN USER", data.sender, state.data.hash);
        if (data.sender === state.data.hash) {
          console.log("HASH match")
          newState.data.projects[curProject].messages = newState.data.projects[curProject].messages.filter((message) => message.hash !== "temp")          
          newState.data.projects[curProject].messages.push(data)
          setState(newState)
        }else{
          newState.data.projects[curProject].messages.push(data)
          setState(newState) 
        }
        if (scrollRef.current) {
          scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
      }
    }
  }, [lastMessage, setMessageHistory]);

  const messagesEndRef = useRef();

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Connected",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Offline",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  if (!state.data) {
    return <div>loading...</div>;
  }

  const sendSocketMessage = (text, attachment = null) => {
    console.log("Attachl", attachment)
    if(!attachment)
      sendMessage(
        JSON.stringify({
          type: "new_message",
          text: text,
          project_hash: state.data.projects[curProject].project_hash,
          data: {},
        })
      );
    else
      sendMessage(
        JSON.stringify({
          type: "new_message",
          text: text,
          project_hash: state.data.projects[curProject].project_hash,
          data: {},
          file_attachment: attachment
        })
      );



    //setState({})
    const newState = JSON.parse(JSON.stringify(state));

    //newState.data.projects[curProject].messages.push({})
    if(!attachment)
      newState.data.projects[curProject].messages.push({
        hash: "temp",
        text: text,
        data: { [selectedLanguage]: text },
        sender: state.data.hash,
        profile_image: state.data.profile_image,
      });
    else
    newState.data.projects[curProject].messages.push({
      hash: "temp",
      text: text,
      data: { [selectedLanguage]: text },
      sender: state.data.hash,
      attachment: attachment,
      profile_image: state.data.profile_image,
    });

    setState(newState);
  };
  
  const isMobile = window.innerWidth < 600;
  
  const reportRequest = (project_hash) => {
    fetch('/api/report', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookiesAsObject().csrftoken,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        project_hash: project_hash
      })
    }).then((res) => {
      if(res.ok){
        // The ai should be replying
      }
    })
  }

  const filteredProjects = state.data.projects.filter((project) =>
    project.name.toLowerCase().includes(inputValue.toLowerCase())
  );
    
  return (
    <main className="flex bg-background max-h-screen h-screen overflow-hidden">
      <nav className="flex-col w-full max-w-[320px] sm:flex hidden"  style={navStyle}>
        <select className="mx-auto w-11/12 select select-ghost">
          <option selected>All Chats</option>
          <option>Contacts</option>
          <option>Groups</option>
          <option>Assistants</option>
        </select>

        <div className="drawer drawer-mobile flex h-full w-full">
          <input id="my-drawer-2" type="checkbox" className="drawer-toggle" />
          <div className="drawer-content flex flex-col items-center justify-center">
            {/* <label
              htmlFor="my-drawer-2"
              className="btn btn-primary drawer-button lg:hidden"
            >
              Open drawer
            </label> */}
          </div>
          <div className="flex flex-col">
            {/* <label htmlFor="my-drawer-2" className="drawer-overlay"></label> */}
            <div className=" mx-auto w-11/12 max-w-[320px]">
              <input
                type="text"
                placeholder="Search..."
                value={inputValue}
                onChange={handleInputChange}
                className=" input w-full  bg-softwhite outline-none"
              />
              {/* {filteredProjects.length > 0 && inputValue && <p className="mt-2 truncate">Results for &apos;{inputValue}&apos;</p>} */}
              {filteredProjects.length < 1 && <p className="mt-2 truncate">Nothing found for &apos;{inputValue}&apos;</p>}
            </div>
            {
              <ul className="menu p-2 w-80 text-base-content">
                {filteredProjects.map((project, index) => (
                  <li
                    key={project.project_hash}
                    onClick={(e) => {
                      setCurProject(index);
                    }}
                  >
                    <div>
                      <div className="avatar">
                        <div className="w-14 rounded-2xl">
                          <img src="/_nstat/group.png" />
                        </div>
                      </div>
                      <div>
                        <p className="text-softwhite font-medium text text-sm">
                          {project.name}
                        </p>
                        <p className="text-grayout text-xs">8 Members</p>
                      </div>
                      {index < 2 && (
                        <svg
                          className="ml-auto"
                          width="24"
                          height="24"
                          viewBox="0 0 24 24"
                          fill="none"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            d="M22.6706 9.29146L14.7644 1.33166C14.3252 0.889447 13.6663 0.889447 13.2271 1.33166C12.7879 1.77387 12.7879 2.43719 13.2271 2.8794L13.4467 3.1005L7.07786 7.63317L3.56401 8.07538C2.46593 8.18593 1.47766 9.07035 1.14824 10.0653C0.818817 11.0603 1.03843 12.2764 1.80709 12.9397L5.65036 16.809L2.90517 19.5729C2.46593 20.0151 2.46593 20.6784 2.90517 21.1206C3.12478 21.3417 3.45421 21.4523 3.67382 21.4523C3.89344 21.4523 4.22286 21.3417 4.44248 21.1206L7.18767 18.3568L11.0309 22.2261C11.58 22.7789 12.2388 23 13.0075 23C13.3369 23 13.6663 23 13.8859 22.8894C14.984 22.5578 15.7527 21.5628 15.8625 20.4573L16.4115 16.9196L19.7058 12.2764C20.0352 11.7236 19.9254 11.0603 19.4861 10.7286C18.9371 10.397 18.2783 10.5075 17.9488 10.9497L14.5448 15.8141C14.435 15.9246 14.435 16.1457 14.3252 16.2563L13.7761 20.0151C13.6663 20.4573 13.3369 20.5678 13.2271 20.6784C13.1173 20.6784 12.7879 20.7889 12.5683 20.5678L7.95633 15.9246L3.45421 11.5025C3.12478 11.2814 3.23459 10.9497 3.23459 10.8392C3.23459 10.7286 3.45421 10.397 3.89344 10.2864L7.6269 9.73367C7.84652 9.73367 7.95633 9.62312 8.06613 9.51256L14.8742 4.64824L21.1333 10.9497C21.3529 11.1709 21.6823 11.2814 21.9019 11.2814C22.1215 11.2814 22.451 11.1709 22.6706 10.9497C23.1098 10.5075 23.1098 9.73367 22.6706 9.29146Z"
                            fill="#7E8085"
                          />
                        </svg>
                      )}
                    </div>
                  </li>
                ))}
              </ul>}
          </div>
        </div>
      </nav>

      <section id="chat" className="w-full px-2 flex flex-col">
        <header className="pt-2 justify-between flex sm:hidden">
          <button onClick={handleHomeClick} id="homebutton" className="btn"><svg className="w-4" viewBox="0 0 24 25" fill="none" xmlns="http://www.w3.org/2000/svg">
<path fill-rule="evenodd" clip-rule="evenodd" d="M5.36364 4.31201C4.63099 4.31201 4 4.95335 4 5.64534V7.88893C4 8.62647 4.59229 9.24052 5.40276 9.31201H7.63636C8.36901 9.31201 9 8.67068 9 7.97868V5.64534C9 4.90202 8.40932 4.31201 7.72727 4.31201H5.36364ZM2 5.64534C2 3.82452 3.55083 2.31201 5.36364 2.31201H7.72727C9.59068 2.31201 11 3.87584 11 5.64534V7.97868C11 9.7995 9.44917 11.312 7.63636 11.312H5.36364C5.34017 11.312 5.31671 11.3112 5.2933 11.3095C3.57427 11.1883 2 9.83427 2 7.88893V5.64534ZM16.3636 4.31201C15.631 4.31201 15 4.95335 15 5.64534V7.97868C15 8.67068 15.631 9.31201 16.3636 9.31201H18.6364C19.369 9.31201 20 8.67068 20 7.97868V5.64534C20 4.90202 19.4093 4.31201 18.7273 4.31201H16.3636ZM13 5.64534C13 3.82452 14.5508 2.31201 16.3636 2.31201H18.7273C20.5907 2.31201 22 3.87585 22 5.64534V7.97868C22 9.7995 20.4492 11.312 18.6364 11.312H16.3636C14.5508 11.312 13 9.7995 13 7.97868V5.64534ZM5.36364 15.312C4.63099 15.312 4 15.9533 4 16.6453V18.9787C4 19.6051 4.56786 20.2386 5.40268 20.312H7.63636C8.36901 20.312 9 19.6707 9 18.9787V16.6453C9 15.902 8.40932 15.312 7.72727 15.312H5.36364ZM2 16.6453C2 14.8245 3.55083 13.312 5.36364 13.312H7.72727C9.59068 13.312 11 14.8758 11 16.6453V18.9787C11 20.7995 9.44917 22.312 7.63636 22.312H5.36364C5.34017 22.312 5.31671 22.3112 5.2933 22.3095C3.59974 22.1901 2 20.8573 2 18.9787V16.6453ZM16.3636 15.312C15.631 15.312 15 15.9533 15 16.6453V18.9787C15 19.6707 15.631 20.312 16.3636 20.312H18.6364C19.369 20.312 20 19.6707 20 18.9787V16.6453C20 15.902 19.4093 15.312 18.7273 15.312H16.3636ZM13 16.6453C13 14.8245 14.5508 13.312 16.3636 13.312H18.7273C20.5907 13.312 22 14.8758 22 16.6453V18.9787C22 20.7995 20.4492 22.312 18.6364 22.312H16.3636C14.5508 22.312 13 20.7995 13 18.9787V16.6453Z" fill="#ddd"/>
</svg>
</button>
          <button className="btn"><svg className="w-4" viewBox="0 0 24 25" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M20.6791 18.3842C19.6769 15.9353 17.7727 14.0985 15.4676 13.1802C16.7705 12.1597 17.5723 10.5271 17.5723 8.7924C17.5723 5.52709 15.0667 2.97607 11.9598 2.97607C8.85296 2.97607 6.34741 5.52709 6.34741 8.69036C6.34741 10.4251 7.14919 12.0577 8.45207 13.0781C6.14697 13.9965 4.24275 15.8332 3.24053 18.2822C2.83964 19.3026 2.93987 20.5271 3.5412 21.4455C4.14253 22.4659 5.24497 22.9761 6.44763 22.9761H17.5723C18.7749 22.9761 19.7772 22.3638 20.4787 21.4455C21.08 20.5271 21.1803 19.4046 20.6791 18.3842ZM8.35185 8.69036C8.35185 6.64954 9.9554 5.01689 11.9598 5.01689C13.9643 5.01689 15.5678 6.64954 15.5678 8.69036C15.5678 10.7312 13.9643 12.3638 11.9598 12.3638C9.9554 12.3638 8.35185 10.7312 8.35185 8.69036ZM18.7749 20.4251C18.4743 20.8332 18.0734 21.1393 17.5723 21.1393H6.34741C5.8463 21.1393 5.44542 20.9353 5.14475 20.4251C4.84408 20.0169 4.84408 19.6087 5.04453 19.2006C6.24719 16.2414 8.95318 14.4046 11.9598 14.4046C14.9665 14.4046 17.6725 16.2414 18.8752 19.0985C19.0756 19.5067 18.9754 20.0169 18.7749 20.4251Z" fill="#ddd"/>
</svg>
</button>
        </header>
        <div className="flex min-h-fit gap-4 items-center m-4">
          <div className="avatar">
            <div className="w-14 relative overflow-visible">
            {connectionStatus === "Connected" ?
              <span className="absolute top-0 right-0 border-background border-solid border-2 inline-flex rounded-full h-3 w-3 bg-green-400"></span>
              : null
            }
              <img className="rounded-2xl" src="/_nstat/group.png" />
            </div>
          </div>
          <div>
            <p className="text-softwhite font-medium text text-sm">
              Designer Team
            </p>
            <p className="text-grayout text-xs">8 Members</p>
          </div>
          <button className="ml-auto text-softwhite font-medium text-base cursor-pointer hover:bg-stone-900 duration-200 rounded p-3">
      {isMobile ? "+ Add" : "+ Invite Member"}
    </button>
        </div>
        <section
          id="chatInner"
          className="w-full bg-darkground p-4 rounded-t-xl flex flex-col justify-end h-full overflow-auto"
        >
          <div className="h-full overflow-scroll scroll-bottom" ref={scrollRef}>
            {state.data.projects[curProject].messages.map((message) => {
              const isSender = message.sender === state.data.hash;
              const chatClass = isSender ? "chat-end" : "chat-start";
              const chatDirection = isSender ? "ml-2" : "mr-2";

              return (
                <div className={`chat ${chatClass}`} key={message.hash}>
                  <div className="chat-image avatar">
                    <div className={`w-12 mt-2 rounded-xl ${chatDirection}`}>
                      <img src={message.profile_image} />
                    </div>
                  </div>
                  <div className="chat-bubble bg-softwhite flex-col gap-1">
                    <p>{(!(message.attachment && message.data[selectedLanguage] == 'file') && message.data[selectedLanguage])}</p>
                    {(message.attachment && isBase64Image(message.attachment)) &&  <img className="max-h max-h-52" src={message.attachment} />}
                    {(message.attachment && !isBase64Image(message.attachment)) &&  <button className="btn flex gap-2" onClick={() => {
                      downloadBase64File(message.attachment, `file.${getFileExtensionFromBase64(message.attachment)}`)
                    }}><svg
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M12 19C11.1969 19 10.4941 18.6946 9.99216 18.0838L4.47059 11.3653C3.96863 10.7545 3.86824 9.83832 4.16941 9.12575C4.47059 8.41317 5.17333 7.90419 5.97647 7.90419H8.28549V4.34132C8.28549 3.01796 9.3898 2 10.6949 2H13.4055C14.7106 2 15.7145 3.01796 15.7145 4.34132V7.90419H18.0235C18.8267 7.90419 19.5294 8.31138 19.8306 9.12575C20.1318 9.83832 20.0314 10.6527 19.5294 11.2635L14.0078 18.0838C13.5059 18.6946 12.8031 19 12 19ZM5.97647 10.0419L11.498 16.7605C11.6988 16.9641 11.8996 16.9641 12 16.9641C12.1004 16.9641 12.3012 16.9641 12.502 16.7605L18.0235 10.0419H14.7106C14.1082 10.0419 13.7067 9.63473 13.7067 9.02395V4.34132C13.7067 4.13772 13.5059 4.03593 13.4055 4.03593H10.6949C10.4941 4.03593 10.2933 4.23952 10.2933 4.34132V8.92216C10.2933 9.53293 9.89177 9.94012 9.28941 9.94012H5.97647V10.0419Z"
                      fill="#D3D3D3"
                    />
                    <path
                      d="M18.4179 22H5.48259C3.49254 22 2 20.5 2 18.5V16C2 15.4 2.39801 15 2.99502 15C3.59204 15 3.99005 15.4 3.99005 16V18.5C3.99005 19.3 4.68657 20 5.48259 20H18.5174C19.3134 20 20.01 19.3 20.01 18.5V16C20.01 15.4 20.408 15 21.005 15C21.602 15 22 15.4 22 16V18.5C21.9005 20.5 20.408 22 18.4179 22Z"
                      fill="#D3D3D3"
                    />
                  </svg>{getFileTypeFromBase64(message.attachment)}</button>}
                  </div>
                </div>
              );
            })}
            <div ref={messagesEndRef} />
          </div>

          <div className="flex bg-softwhite rounded-2xl align-middle p-1 w-full mt-4 gap-4">
            <input
              id="chatInput"
              type="text"
              placeholder="Type here"
              className="input w-full bg-softwhite outline-none"
              onChange={(e) => {
                setInputState(e.target.value);
              }}
              onKeyPress={(e) => {
                // we need to check if a file is present, then we would also send the b64 encoded file
                // 
                console.log("SEND triggered")
                if( document.getElementById("fileUpload").files.length == 0 ){
                    console.log("no files selected");

                    if (
                      e.key === "Enter" &&
                      !e.shiftKey &&
                      document.getElementById("chatInput").value != ""
                    ) {
                      e.preventDefault();
                      document.getElementById("chatInput").value = "";
                      sendSocketMessage(inputState);
                    }
                }else{
                  console.log("files selected", );
                  getBase64(document.getElementById("fileUpload").files[0]).then(
                    data => {
                      console.log("File converted", data)
                      sendSocketMessage("file", data);
                    }
                  )
                }
              }}
            />
            
            <button className="rounded-r-xl rounded-l-4xl bg-transparent" onClick={handleClick}>
            <svg width="24" height="28" viewBox="0 0 24 28" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 15.7502C20.4 15.7502 20 16.2168 20 16.9168V19.8335C20 21.8168 18.6 23.4502 16.9 23.4502H7.1C5.4 23.3335 4 21.7002 4 19.7168V8.2835C4 6.30016 5.4 4.66683 7.1 4.66683H11.1C11.3 4.66683 11.6 4.66683 11.8 4.7835V8.2835C11.8 11.5502 14.1 14.2335 16.9 14.2335H21C21.4 14.2335 21.8 14.0002 21.9 13.5335C22.1 13.0668 22 12.6002 21.7 12.2502L14.7 4.0835C13.7 2.91683 12.5 2.3335 11.1 2.3335H7.1C4.3 2.3335 2 5.01683 2 8.2835V19.7168C2 22.9835 4.3 25.6668 7.1 25.6668H16.9C19.7 25.6668 22 22.9835 22 19.7168V16.8002C22 16.2168 21.6 15.7502 21 15.7502ZM13.8 6.30016L18.6 11.9002H16.9C15.2 11.9002 13.8 10.2668 13.8 8.2835V6.30016Z" fill="#181A1E"/>
            </svg>
          </button>
          <input type="file" className="file-input file-input-bordered w-full max-w-xs hidden" id="fileUpload" ref={fileInputRef} />

            <button
              className="btn rounded-r-xl rounded-l-4xl"
              onClick={(e) => {
                if (document.getElementById("chatInput").value != "") {
                  document.getElementById("chatInput").value = "";
                  sendSocketMessage(inputState);
                }
              }}
            >
              <svg
                className="red fill-white text-white"
                width="24"
                height="25"
                viewBox="0 0 24 25"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M12.2148 21.296C11.6963 21.296 11.2815 21.196 10.763 20.9961C9.62222 20.4962 9 19.3966 9 18.197V6.40064C9 5.20101 9.72593 4.20133 10.8667 3.60151C12.0074 3.10167 13.3556 3.20164 14.2889 4.00139L21.8593 9.89955C22.5852 10.4994 23 11.2991 23 12.2988C23 13.1985 22.5852 14.0982 21.8593 14.698L14.2889 20.5962C13.6667 21.0961 12.9407 21.296 12.2148 21.296ZM11.6963 5.40095C11.4889 5.50092 11.0741 5.80083 11.0741 6.40064V18.2969C11.0741 18.8967 11.4889 19.1966 11.6963 19.2966C12.1111 19.4966 12.6296 19.3966 12.9407 19.1966L20.5111 13.2985C20.8222 13.0985 20.9259 12.7986 20.9259 12.4987C20.9259 12.1988 20.8222 11.8989 20.5111 11.699L12.9407 5.80083C12.5259 5.30098 12.0074 5.30098 11.6963 5.40095Z" />
                <path d="M6 18.296C5.4 18.296 5 17.896 5 17.296V7.29599C5 6.69599 5.4 6.29599 6 6.29599C6.6 6.29599 7 6.69599 7 7.29599V17.296C7 17.896 6.6 18.296 6 18.296Z" />
                <path d="M2 16.296C1.4 16.296 1 15.896 1 15.296V9.29599C1 8.69599 1.4 8.29599 2 8.29599C2.6 8.29599 3 8.69599 3 9.29599V15.296C3 15.896 2.6 16.296 2 16.296Z" />
              </svg>
            </button>
          </div>
        </section>
      </section>

      <section className="flex content-center align-middle flex-col justify-center min-w-fit px-12 gap-4 lg:flex hidden">
        <p className="text-softwhite font-medium text-xl">You</p>
        <div className="profile">
          <img className="w-24 rounded-full" src={state.data.profile_image} />
          <p className="text-softwhite font-medium text text-xl">Nihao Sano</p>
          <p className="text-grayout text-xs capitalize">{state.data.language}</p>
        </div>
        <div className="flex flex-col gap-2">
        <FlagComponent country="serbian" />
          <div className="dropdown dropdown-end">
            <button className="btn gap-2">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M22 15.2998C21.4 15.2998 21 15.6998 21 16.2998V18.9998C21 20.0998 20.1 21.0998 18.9 21.0998H16.2C15.6 21.0998 15.2 21.4998 15.2 22.0998C15.2 22.6998 15.6 23.0998 16.2 23.0998H18.9C21.1 23.0998 23 21.2998 23 18.9998V16.2998C23 15.6998 22.6 15.2998 22 15.2998Z"
                  fill="#D3D3D3"
                />
                <path
                  d="M7.8 21.0002H5.1C3.9 21.0002 3 20.1002 3 18.9002V16.2002C3 15.6002 2.6 15.2002 2 15.2002C1.4 15.2002 1 15.6002 1 16.2002V18.9002C1 21.2002 2.8 23.0002 5.1 23.0002H7.8C8.4 23.0002 8.8 22.6002 8.8 22.0002C8.8 21.4002 8.3 21.0002 7.8 21.0002Z"
                  fill="#D3D3D3"
                />
                <path
                  d="M2 8.8C2.6 8.8 3 8.4 3 7.8V5.1C3 3.9 3.9 3 5.1 3H7.8C8.4 3 8.8 2.6 8.8 2C8.8 1.4 8.4 1 7.8 1H5.1C2.8 1 1 2.8 1 5.1V7.8C1 8.3 1.4 8.8 2 8.8Z"
                  fill="#D3D3D3"
                />
                <path
                  d="M18.9 1H16.2C15.6 1 15.2 1.4 15.2 2C15.2 2.6 15.6 3 16.2 3H18.9C20.1 3 21 3.9 21 5.1V7.8C21 8.4 21.4 8.8 22 8.8C22.6 8.8 23 8.4 23 7.8V5.1C23 2.8 21.2 1 18.9 1Z"
                  fill="#D3D3D3"
                />
                <path
                  d="M18.2 9.9C18.8 9.9 19.2 9.5 19.2 8.9V7.3C19.2 6.3 18.4 5.5 17.4 5.5H6.59999C5.59999 5.5 4.79999 6.3 4.79999 7.3V9C4.79999 9.6 5.19999 10 5.79999 10C6.39999 10 6.79999 9.6 6.79999 9V7.5H9.09999V17.2H7.99999C7.39999 17.2 6.99999 17.6 6.99999 18.2C6.99999 18.8 7.39999 19.2 7.99999 19.2H16C16.6 19.2 17 18.8 17 18.2C17 17.6 16.6 17.2 16 17.2H14.8V7.5H17.1V8.9C17.2 9.5 17.6 9.9 18.2 9.9ZM12.8 17.2H11.1V7.5H12.8V17.2Z"
                  fill="#D3D3D3"
                />
              </svg>
              Change Language
            </button>
            <ul
              tabIndex={0}
              className="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52 overflow-scroll h-60 flex flex-col flex-nowrap"
            >
              {state.data.projects[curProject].languages.map((lang, index) => {
                return (
                  <li key={index} className="capitalize">
                    <a
                      onClick={() => {
                        console.log("CHANGED LANG", lang);
                        setSelectedLanguage(lang);
                      }}
                    >
                      {lang}
                    </a>
                  </li>
                );
              })}
            </ul>
          </div>
          <button className="btn gap-2" onClick={() => {
            reportRequest(state.data.projects[curProject].project_hash)
          }}>
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 19C11.1969 19 10.4941 18.6946 9.99216 18.0838L4.47059 11.3653C3.96863 10.7545 3.86824 9.83832 4.16941 9.12575C4.47059 8.41317 5.17333 7.90419 5.97647 7.90419H8.28549V4.34132C8.28549 3.01796 9.3898 2 10.6949 2H13.4055C14.7106 2 15.7145 3.01796 15.7145 4.34132V7.90419H18.0235C18.8267 7.90419 19.5294 8.31138 19.8306 9.12575C20.1318 9.83832 20.0314 10.6527 19.5294 11.2635L14.0078 18.0838C13.5059 18.6946 12.8031 19 12 19ZM5.97647 10.0419L11.498 16.7605C11.6988 16.9641 11.8996 16.9641 12 16.9641C12.1004 16.9641 12.3012 16.9641 12.502 16.7605L18.0235 10.0419H14.7106C14.1082 10.0419 13.7067 9.63473 13.7067 9.02395V4.34132C13.7067 4.13772 13.5059 4.03593 13.4055 4.03593H10.6949C10.4941 4.03593 10.2933 4.23952 10.2933 4.34132V8.92216C10.2933 9.53293 9.89177 9.94012 9.28941 9.94012H5.97647V10.0419Z"
                fill="#D3D3D3"
              />
              <path
                d="M18.4179 22H5.48259C3.49254 22 2 20.5 2 18.5V16C2 15.4 2.39801 15 2.99502 15C3.59204 15 3.99005 15.4 3.99005 16V18.5C3.99005 19.3 4.68657 20 5.48259 20H18.5174C19.3134 20 20.01 19.3 20.01 18.5V16C20.01 15.4 20.408 15 21.005 15C21.602 15 22 15.4 22 16V18.5C21.9005 20.5 20.408 22 18.4179 22Z"
                fill="#D3D3D3"
              />
            </svg>
            Get Report
          </button>
        </div>
      </section>
    </main>
  );
}
