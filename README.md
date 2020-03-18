# GitHub Contributions API

GitHub doesn't have an API for contribution data so I made my own.

https://vlad-munteanu.appspot.com

## Usage

'GET /contributions/<username>/<userCreationYear>'
Returns json data of all contribution history
(The user creation year is sent to the api as a parameter here instead of automatically being found because of GitHub's api limit.)

'GET /dayCount/<username>/<date>'
Returns the data for a given day's contributions. Returns the data for today's contributions if the optional date parameter is not given.

'GET /weeklyCount/<username>/'
Returns the data for current week's contributions

'GET /monthlyCount/<username>/'
Returns the data for the last 30 days of contributions

## Authors

- **Vlad Munteanu**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

## TO_DO

- [ ] Add Montly contributions
- [ ] FIX TODAY COUNT WHY IS THIS NOT WORKING
- [ ] Contributions fetches tomorrows date too
- [ ] Add Weekly contributions
- [ ] Completely remove dependence on GitHub's API (since they have a limit on unauthorized api requests)

## Questions

If you have any questions about this repository, or any others of mine, please
don't hesitate to contact me.
