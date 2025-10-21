class Music {
  final String name;
  final String link;
  final String artist;
  final String imageLink;

  Music(
      {required this.name,
        required this.link,
        required this.artist,
        required this.imageLink});

  factory Music.fromJson(Map data) => Music(
      name: data['name'],
      link: data['link'],
      artist: data['artist'],
      imageLink: data['image_link']);
}