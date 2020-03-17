let initialTab = 'bluetooth'; // tab to be active at start
let player = {
  // Current player value; call updatePlayer() after changing
  active: false,
  current: 0,
  length: 1,
  playing: false
};

/**
 * List Bluetooth devices
 * @param {Array} list - Array of objects with properties `name` and `status`
 */
const listBluetoothDevices = (list) => {
  const parent = document.querySelector('#bluetooth .panel');
  parent.querySelectorAll('.panel-block').forEach((el) => el.remove());

  if (!list || list.length === 0) {
    let el = document.createElement('p');
    el.classList.add('panel-block');
    el.innerText = 'No devices found';
    parent.appendChild(el);
  } else {
    list.forEach((i) => {
      let el = document.createElement('p');
      el.classList.add('panel-block');
      el.innerHTML = `<span class="fa fa-fw fa-bluetooth"></span> ${i.name} (${i.status})`;
      parent.appendChild(el);
    });
  }
};

/**
 * Prints time in seconds as string
 */
const timeString = (s) => {
  let hr = Math.floor(s/(60*60));
  let min = `${Math.floor((s % (60*60))/60)}`;
  let sec = `${Math.floor(s%60)}`;
  if(sec.length === 1) sec = `0${sec}`;

  if (hr === 0) {
    return `${min}:${sec}`;
  } else {
    if(min.length === 1) min = `0${min}`;
    return `${hr}:${min}:${sec}`;
  }
};
/**
 * Update player
 */
const updatePlayer = () => {
  let div = document.querySelector('footer');

  if (player.active && div.classList.contains('is-hidden')) {
    div.classList.remove('is-hidden');
  } else if (!player.active && !div.classList.contains('is-hidden')) {
    div.classList.add('is-hidden');
    return;
  }

  let playBtn = document.querySelector('footer .fa-play');
  let pauseBtn = document.querySelector('footer .fa-pause');
  if (player.playing) {
    pauseBtn.classList.remove('is-hidden');
    playBtn.classList.add('is-hidden');
  } else {
    pauseBtn.classList.add('is-hidden');
    playBtn.classList.remove('is-hidden');
  }

  const current = timeString(player.current);
  const length = timeString(player.length);

  let timeBar = document.querySelector('footer progress');
  timeBar.setAttribute('value', `${Math.floor(player.current / player.length * 100)}`);
  let timeEl = document.querySelector('footer #audio-time');
  timeEl.innerText = `${current}/${length}`;
}

/** 
 * Updates active section
 */
const updateSection = (name) => {
  document.querySelectorAll('section').forEach((el) => {
    el.classList.add('is-hidden');
  });

  if(!!name) {
    document.querySelector(`section#${name}`).classList.remove('is-hidden');
  }
}

/**
 * Initialize app
 * * Set up tabs
 * * Set up media player
 */
const init = () => {
  let tabs = document.querySelectorAll('header li');
  tabs.forEach((el) => {
    el.querySelector('a').addEventListener('click', (evt) => {
      tabs.forEach((t) => t.classList.remove('is-active'));
      evt.target.parentNode.classList.add('is-active');
      updateSection(evt.target.getAttribute('data-section'));
    });
  });


  listBluetoothDevices();
  updatePlayer();
  updateSection(initialTab);
};

window.addEventListener('load', init);