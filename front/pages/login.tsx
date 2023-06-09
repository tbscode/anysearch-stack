import Image from 'next/image'
import { Inter } from 'next/font/google'
import { useRouter } from 'next/router';
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

export const getServerSideProps = async ({ req }: { req: any }) => {
  if (req.method == "POST") {
    const streamPromise = new Promise((resolve, reject) => {
      let body = ''
      req.on('data', (chunk: any) => {
        body += chunk
      })
      req.on('end', () => {
        console.log(body);
        resolve(body)
      });
    });
    const res = await streamPromise;
    if (typeof res !== "string") throw new Error("Not a string")
    return { props: { data: JSON.parse(res) } };
  }
  return { props: {} };
};

export default function Index({ state, updateTheme }): JSX.Element {
  const router = useRouter();

  const [loginData, setLoginData] = useState({
    username: '',
    password: ''
  })

  const loginRequest = () => {
    fetch('/api/login', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookiesAsObject().csrftoken,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(loginData)
    }).then((res) => {
      if(res.ok){
        window.location.href = "/chat";
      }
    })
  }
  //hello alter
  return (
    <main className='flex flex-col justify-center items-center w-screen h-screen'>
      <svg className='w-56' viewBox="0 0 1182 1182" version="1.1" xmlns="http://www.w3.org/2000/svg" style={{ fillRule: 'evenodd', clipRule: 'evenodd', strokeLinejoin: 'round', strokeMiterlimit: 2 }}
      ><rect id="Artboard3" x="0" y="0" width="1181.1" height="1181.1" style={{ fill: 'none' }}
        /><g id="Logo-farbig"><g><path d="M187.43,839.851l-28.236,0l51.45,-136.37l32.63,-0l51.45,136.37l-28.236,0l-38.959,-108.404l-1.14,0l-38.959,108.404Zm0.913,-53.483l77.005,0l0,19.87l-77.005,0l-0,-19.87Z" style={{ fill: '#ccc', fillRule: 'nonzero' }}
        /><path d="M329.12,779.923l-0,59.928l-25.84,0l-0,-102.278l24.699,0l-0,17.366l1.312,0c2.491,-5.708 6.508,-10.252 12.05,-13.63c5.542,-3.378 12.401,-5.067 20.577,-5.067c7.549,-0 14.138,1.507 19.766,4.521c5.628,3.014 10.001,7.387 13.119,13.118c3.119,5.731 4.668,12.689 4.649,20.875l-0,65.095l-25.84,0l-0,-61.366c0.019,-6.845 -1.868,-12.197 -5.661,-16.054c-3.794,-3.858 -9.018,-5.787 -15.673,-5.787c-4.516,0 -8.516,0.915 -12,2.744c-3.484,1.829 -6.21,4.479 -8.178,7.95c-1.967,3.472 -2.961,7.666 -2.98,12.585Z" style={{ fill: '#ccc', fillRule: 'nonzero' }}
          /><path d="M434.399,873.238l13.423,-31.256l-39.7,-104.409l27.38,0l25.212,77.242l1.141,-0l25.326,-77.242l27.494,0l-43.865,114.637l-8.955,21.028l-4.201,9.966" style={{ fill: '#ccc', fillRule: 'nonzero' }}
          /><path d="M711.239,749.506l-26.696,0c-0.741,-4.093 -2.131,-7.724 -4.171,-10.894c-2.039,-3.169 -4.587,-5.861 -7.644,-8.077c-3.056,-2.215 -6.523,-3.895 -10.402,-5.04c-3.879,-1.145 -8.033,-1.718 -12.463,-1.718c-7.967,0 -15.014,1.856 -21.142,5.567c-6.127,3.711 -10.923,9.131 -14.388,16.26c-3.465,7.129 -5.198,15.817 -5.198,26.062c0,10.423 1.743,19.195 5.227,26.315c3.485,7.12 8.285,12.496 14.403,16.127c6.117,3.631 13.112,5.447 20.983,5.447c4.373,-0 8.48,-0.546 12.321,-1.638c3.841,-1.092 7.295,-2.705 10.36,-4.84c3.066,-2.136 5.647,-4.755 7.743,-7.858c2.097,-3.103 3.554,-6.652 4.371,-10.647l26.696,0.106c-0.988,6.49 -3.137,12.581 -6.445,18.272c-3.309,5.691 -7.63,10.696 -12.963,15.016c-5.334,4.319 -11.563,7.69 -18.689,10.114c-7.125,2.424 -15.037,3.636 -23.736,3.636c-12.834,-0 -24.285,-2.779 -34.353,-8.337c-10.067,-5.558 -18.001,-13.566 -23.8,-24.025c-5.799,-10.458 -8.699,-23.021 -8.699,-37.688c0,-14.703 2.924,-27.279 8.77,-37.728c5.847,-10.45 13.809,-18.449 23.886,-23.998c10.078,-5.549 21.476,-8.324 34.196,-8.324c8.11,0 15.661,1.07 22.653,3.21c6.992,2.14 13.226,5.263 18.702,9.369c5.476,4.106 9.982,9.118 13.519,15.035c3.536,5.918 5.856,12.676 6.959,20.276Z" style={{ fill: '#ccc', fillRule: 'nonzero' }}
          /><path d="M756.929,779.923l-0,59.928l-25.84,0l-0,-136.37l25.269,-0l0,51.458l1.313,0c2.529,-5.78 6.491,-10.341 11.886,-13.683c5.395,-3.343 12.29,-5.014 20.684,-5.014c7.577,-0 14.194,1.489 19.851,4.468c5.657,2.979 10.051,7.333 13.184,13.064c3.132,5.731 4.689,12.725 4.669,20.982l0,65.095l-25.84,0l0,-61.366c0.019,-6.899 -1.865,-12.263 -5.654,-16.094c-3.789,-3.831 -9.072,-5.747 -15.85,-5.747c-4.582,0 -8.658,0.915 -12.228,2.744c-3.57,1.829 -6.365,4.479 -8.385,7.95c-2.02,3.472 -3.04,7.666 -3.059,12.585Z" style={{ fill: '#ccc', fillRule: 'nonzero' }}
          /><path d="M881.279,841.929c-6.96,0 -13.206,-1.17 -18.739,-3.509c-5.533,-2.34 -9.906,-5.793 -13.119,-10.361c-3.214,-4.568 -4.82,-10.208 -4.82,-16.92c-0,-5.753 1.15,-10.523 3.451,-14.31c2.3,-3.786 5.423,-6.812 9.369,-9.076c3.945,-2.264 8.397,-3.975 13.355,-5.133c4.958,-1.159 10.094,-2.004 15.408,-2.537c6.445,-0.657 11.662,-1.241 15.651,-1.752c3.988,-0.51 6.893,-1.307 8.713,-2.39c1.82,-1.083 2.731,-2.775 2.731,-5.074l-0,-0.427c-0,-5.007 -1.586,-8.886 -4.756,-11.639c-3.171,-2.752 -7.765,-4.128 -13.783,-4.128c-6.322,-0 -11.322,1.292 -15.001,3.875c-3.68,2.584 -6.17,5.625 -7.472,9.123l-24.072,-3.196c1.901,-6.215 5.041,-11.42 9.419,-15.615c4.378,-4.195 9.725,-7.347 16.043,-9.455c6.317,-2.109 13.307,-3.163 20.97,-3.163c5.248,-0 10.493,0.575 15.736,1.724c5.243,1.15 10.03,3.052 14.36,5.707c4.331,2.655 7.812,6.246 10.446,10.774c2.633,4.528 3.95,10.179 3.95,16.953l-0,68.451l-24.813,0l-0,-14.063l-0.856,-0c-1.56,2.859 -3.761,5.518 -6.603,7.977c-2.842,2.46 -6.384,4.435 -10.624,5.927c-4.24,1.491 -9.222,2.237 -14.944,2.237Zm6.673,-17.739c5.191,-0 9.69,-0.963 13.498,-2.89c3.807,-1.926 6.75,-4.483 8.827,-7.67c2.077,-3.188 3.115,-6.681 3.115,-10.482l0,-12.038c-0.846,0.639 -2.222,1.223 -4.128,1.751c-1.906,0.528 -4.055,0.994 -6.446,1.398c-2.39,0.404 -4.753,0.76 -7.087,1.066c-2.334,0.306 -4.356,0.57 -6.068,0.792c-3.84,0.497 -7.279,1.299 -10.317,2.404c-3.037,1.105 -5.433,2.646 -7.187,4.621c-1.754,1.976 -2.631,4.517 -2.631,7.624c0,4.412 1.733,7.753 5.198,10.021c3.465,2.269 7.874,3.403 13.226,3.403Z" style={{ fill: '#ccc', fillRule: 'nonzero' }}
          /><path d="M1017.66,737.573l0,18.645l-62.916,-0l0,-18.645l62.916,0Zm-47.401,-24.504l25.84,0l0,96.046c0,3.232 0.525,5.698 1.576,7.398c1.051,1.7 2.458,2.863 4.221,3.489c1.763,0.626 3.729,0.939 5.897,0.939c1.587,-0 3.056,-0.114 4.406,-0.34c1.35,-0.227 2.391,-0.415 3.123,-0.567l4.335,18.805c-1.388,0.435 -3.346,0.921 -5.875,1.458c-2.529,0.537 -5.628,0.85 -9.298,0.939c-6.465,0.178 -12.285,-0.746 -17.462,-2.77c-5.176,-2.024 -9.274,-5.158 -12.292,-9.402c-3.019,-4.243 -4.509,-9.579 -4.471,-16.008l0,-99.987Z" style={{ fill: '#ccc', fillRule: 'nonzero' }}
          /></g><path d="M401.326,556.292c0,65.211 52.864,118.075 118.075,118.075l460.665,0c0,0 -23.216,-40.574 -38.502,-67.29c-8.582,-14.997 -13.096,-31.975 -13.096,-49.254l0,-72.435c0,-65.229 -52.878,-118.107 -118.107,-118.107l-291.025,-0c-31.298,-0 -61.315,12.433 -83.446,34.564c-22.131,22.131 -34.564,52.147 -34.564,83.445l0,71.002Zm39.584,0l-0,-71.002c-0,-20.8 8.262,-40.748 22.97,-55.456c14.708,-14.707 34.656,-22.97 55.456,-22.97l291.025,-0c43.367,-0 78.524,35.156 78.524,78.524c-0,-0 -0,72.435 -0,72.435c-0,24.175 6.316,47.93 18.322,68.913c-0,0 4.605,8.048 4.605,8.048c-96.509,-0 -274.236,-0 -392.411,-0c-43.349,-0 -78.491,-35.142 -78.491,-78.492Z" style={{ fill: "url(#_Linear1)" }}
          /><path d="M767.468,482.426c0,65.211 -52.864,118.075 -118.075,118.075l-460.665,0c-0,0 23.216,-40.574 38.503,-67.29c8.581,-14.997 13.095,-31.975 13.095,-49.254l0,-72.435c0,-65.229 52.879,-118.108 118.107,-118.108c86.801,0 204.248,0 291.026,0c31.298,0 61.314,12.433 83.445,34.565c22.131,22.131 34.564,52.147 34.564,83.445l0,71.002Zm-39.583,-0c-0,43.35 -35.142,78.492 -78.492,78.492l-392.41,-0c-0,-0 4.604,-8.048 4.604,-8.048c12.007,-20.983 18.323,-44.738 18.323,-68.913l-0,-72.435c-0,-43.368 35.156,-78.524 78.523,-78.524c0.001,-0 291.026,-0 291.026,-0c20.8,-0 40.748,8.262 55.455,22.97c14.708,14.708 22.971,34.656 22.971,55.456l-0,71.002Z" style={{ fill: "url(#_Linear2)" }}
          /><g><path className='animate-wiggle' d="M534.314,508.604c-4.3,0 -7.983,-1.525 -11.051,-4.574c-3.068,-3.05 -4.593,-6.734 -4.574,-11.052c-0.019,-4.261 1.506,-7.912 4.574,-10.951c3.068,-3.04 6.751,-4.56 11.051,-4.56c4.185,0 7.831,1.52 10.938,4.56c3.106,3.039 4.668,6.69 4.687,10.951c-0.019,2.87 -0.75,5.488 -2.194,7.856c-1.445,2.367 -3.338,4.254 -5.682,5.661c-2.344,1.406 -4.927,2.109 -7.749,2.109Z" style={{ fill: '#ccc', fillRule: 'nonzero'}}
          /><path className='animate-wiggle'  d="M589.427,508.604c-4.299,0 -7.982,-1.525 -11.051,-4.574c-3.068,-3.05 -4.592,-6.734 -4.574,-11.052c-0.018,-4.261 1.506,-7.912 4.574,-10.951c3.069,-3.04 6.752,-4.56 11.051,-4.56c4.186,0 7.832,1.52 10.938,4.56c3.106,3.039 4.669,6.69 4.687,10.951c-0.018,2.87 -0.75,5.488 -2.194,7.856c-1.444,2.367 -3.338,4.254 -5.682,5.661c-2.343,1.406 -4.926,2.109 -7.749,2.109Z" style={{ fill: '#ccc', fillRule: 'nonzero', animationDelay: '.2s'}}
            /><path className='animate-wiggle' d="M644.541,508.604c-4.299,0 -7.983,-1.525 -11.051,-4.574c-3.068,-3.05 -4.593,-6.734 -4.574,-11.052c-0.019,-4.261 1.506,-7.912 4.574,-10.951c3.068,-3.04 6.752,-4.56 11.051,-4.56c4.186,0 7.832,1.52 10.938,4.56c3.106,3.039 4.668,6.69 4.687,10.951c-0.019,2.87 -0.75,5.488 -2.194,7.856c-1.444,2.367 -3.338,4.254 -5.682,5.661c-2.344,1.406 -4.927,2.109 -7.749,2.109Z" style={{ fill: '#ccc', fillRule: 'nonzero', animationDelay: '.4s'}}
            /></g></g><defs><linearGradient id="_Linear1" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(578.74,0,0,307.087,401.326,520.824)"><stop offset="0" style={{ stopColor: "#8caf8f", stopOpacity: 1 }}
            /><stop offset="1" style={{ stopColor: '#2caf8f', stopOpacity: '1' }}
              /></linearGradient><linearGradient id="_Linear2" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(-578.74,0,0,307.087,767.468,446.958)"><stop offset="0" style={{ stopColor: "#2c598f", stopOpacity: 1 }}
              /><stop offset="1" style={{ stopColor: '#e2af8f', stopOpacity: 1 }}
            /></linearGradient></defs></svg>

      <div className='flex flex-col gap-2 w-full max-w-md'>
        <input type="text" placeholder="Username" onChange={(e) => { setLoginData({ ...loginData, username: e.target.value }) }} className="input input-bordered input-sm w-full p-4 py-6" />
        <input type="password" placeholder="Password" onChange={(e) => { setLoginData({ ...loginData, password: e.target.value }) }} className="input input-bordered input-sm w-full p-4 py-6" />
        <button className="btn w-full" onClick={() => { loginRequest(); }}>Login</button>
      </div>
    </main>);
}
