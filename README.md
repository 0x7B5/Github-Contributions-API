# GitHub Contributions API

GitHub doesn't have an API for contribution data so I made my own.

https://vlad-munteanu.appspot.com

## Usage

'GET /contributions/<username>/<userCreationYear>'
Returns json data of all contribution history
(The user creation year is sent to the api as a parameter here instead of automatically being found because of GitHub's api limit.)

'GET /todayCount/<username>'
Returns the count of contributions for today

## Authors

- **Vlad Munteanu**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

## Questions

If you have any questions about this repository, or any others of mine, please
don't hesitate to contact me.
