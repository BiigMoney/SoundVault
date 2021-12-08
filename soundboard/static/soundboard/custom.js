let audio = null
let playing = null

function playSound(link) {
  if (audio) audio.pause()

  if (playing && link === playing) {
    document.getElementById(link).innerHTML = '<span><i class="bi bi-play-fill"></i></span>'
    playing = null
    return
  } else if (playing && playing === audio.file) {
    document.getElementById(playing).innerHTML = '<span><i class="bi bi-play-fill"></i></span>'
  }

  audio = new Audio(link)
  playing = link
  audio.file = link
  document.getElementById(link).innerHTML = '<span><i class="bi bi-pause-btn"></i></span>'

  audio.addEventListener("ended", event => {
    currentAudio = event.path[0]
    if (currentAudio.file === playing && currentAudio.file) {
      playing = null
      document.getElementById(currentAudio.file).innerHTML = '<span><i class="bi bi-play-fill"></i></span>'
    }
  })

  audio.play().catch(err => console.error("handle it", err))
}
