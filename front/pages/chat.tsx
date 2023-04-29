import Image from "next/image";
import { Inter } from "next/font/google";

export const getCookiesAsObject = () => {
  // stolen: https://stackoverflow.com/a/64472572
  return Object.fromEntries(
    document.cookie
      .split("; ")
      .map((v) => v.split(/=(.*)/s).map(decodeURIComponent))
  );
};

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

export default function Index({ state, updateTheme }): JSX.Element {
  console.log("STATE", state);

  return (
    <main className="flex bg-background max-h-screen overflow-hidden">
      <nav>
        <select className="select select-ghost w-full max-w-xs">
          <option selected>All Chats</option>
          <option>Contacts</option>
          <option>Groups</option>
          <option>Assistants</option>
        </select>

        <div className="drawer drawer-mobile">
          <input id="my-drawer-2" type="checkbox" className="drawer-toggle" />
          <div className="drawer-content flex flex-col items-center justify-center">
            <label
              htmlFor="my-drawer-2"
              className="btn btn-primary drawer-button lg:hidden"
            >
              Open drawer
            </label>
          </div>
          <div className="drawer-side">
            <label htmlFor="my-drawer-2" className="drawer-overlay"></label>
            <ul className="menu p-4 w-80 text-base-content">
            {[...Array(10)].map((_, index) => (
                <li key={index}>
                    <div>
                    <div className="avatar">
                        <div className="w-16 rounded-2xl">
                            <img src="/group.png" />
                        </div>
                    </div>
                    <div>
                        <p className="text-softwhite font-medium text text-sm">Designer Team</p>
                        <p className="text-grayout text-xs">8 Members</p>
                    </div>
                    </div>
                </li>
                ))}
            </ul>
          </div>
        </div>
      </nav>

      <section id="chat" className="bg-darkground w-full p-8 rounded-t-lg flex flex-col justify-end">

        {[...Array(2)].map((_, index) => (
        <div key={index} className="chat chat-start">
          <div className="chat-image avatar">
            <div className="w-10 rounded-full">
              <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Frevgineer.com%2Fwp-content%2Fuploads%2F2019%2F12%2FThisPersonDoesNotExist_fail2-768x811.jpg&f=1&nofb=1&ipt=b88a3d792b206b14cb27c58ef847d473ce09ec6a69ffc6b6db5c280bf0ea12dd&ipo=images" />
            </div>
          </div>
          <div className="chat-bubble bg-softwhite">
            It was you who would bring balance to the Force
          </div>
        </div>
        ))}
        {[...Array(2)].map((_, index) => (
        <div className="chat chat-end" key={index}>
          <div className="chat-image avatar">
            <div className="w-10 rounded-full">
              <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Frevgineer.com%2Fwp-content%2Fuploads%2F2019%2F12%2FThisPersonDoesNotExist_fail2-768x811.jpg&f=1&nofb=1&ipt=b88a3d792b206b14cb27c58ef847d473ce09ec6a69ffc6b6db5c280bf0ea12dd&ipo=images" />
            </div>
          </div>
          <div className="chat-bubble bg-softwhite">
            It was you who would bring balance to the Force
          </div>
        </div>
        ))}

        <div className="flex bg-softwhite rounded-2xl align-middle p-1 w-full mt-4">
            <input
            type="text"
            placeholder="Type here"
            className="input w-full outline-none bg-softwhite"
            />
            <button className="btn ">Hello daisyUI</button>
        </div>
      </section>
    </main>
  );
}
