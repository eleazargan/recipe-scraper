import React, { Component } from 'react';

class Search extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            menu: '',
            servings: '',
            ingredients: [],
            directions: [],
            search: false,
            loading: false,
            coverImage: ''
        };

        this._onUpdateMenu = this._onUpdateMenu.bind(this);
        this._searchMenu = this._searchMenu.bind(this);
    }

    _onUpdateMenu(event) {
        this.setState({ menu: event.target.value });
    }

    async _searchMenu() {
        this.setState({
            search: true,
            loading: true
        });

        const url = '//localhost:5000/search?search_term=' + this.state.menu;

        try {
            const response = await fetch(url, {
                method: 'get',
                headers: { 'Access-Control-Allow-Origin': '*' },
            });
            const json = await response.json();
            this.setState({
                servings: json.serving,
                ingredients: json.ingredients,
                coverImage: json.image,
                directions: json.directions,
                loading: false
            });
        } catch (err) {
            this.setState({
                loading: false
            });
        }
    }

    convertUnicode(input) {
        return input.replace(/\\u(\w\w\w\w)/g, function (a, b) {
            var charcode = parseInt(b, 16);
            return String.fromCharCode(charcode);
        });
    }

    render() {
        return (
            <div className="max-w-md overflow-hidden shadow-md m-auto">
                <nav className="flex items-center justify-between flex-wrap bg-purple-500 p-6 text-center">
                    <div className="w-full block flex-grow lg:w-auto">
                        <div className="text-sm lg:flex-grow m-auto">
                            <input className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-auto py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-w-hite focus:border-purple-500"
                                type="text" placeholder="Search for recipes" value={this.state.menu}
                                onChange={this._onUpdateMenu} />
                            <button className="shadow bg-purple-900 hover:bg-purple-800 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded"
                                type="button" onClick={this._searchMenu}>
                                Search Recipe
                    </button>
                        </div>
                    </div>
                </nav>
                {this.state.loading ? <div>
                    Searching for your food!
                </div> :
                    <div>
                        <img className="w-full" src={this.state.coverImage} alt={this.state.menu} />
                        <div className="px-6 py-4">
                            <div className="font-bold text-xl mb-2">{this.state.search && (this.state.menu)}</div>
                            {this.state.search && (<p className="mb-4 font-bold">Servings: {this.state.servings} person</p>)}
                            {(this.state.search && this.state.ingredients) && (
                                <div className="mb-8 px-4">
                                    <div className="mb-2 text-xl text-bold">Ingredients</div>
                                    <ul className="list-disc">
                                        {this.state.ingredients.map((item, index) => (
                                            <li>{this.convertUnicode(item)}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                            {(this.state.search && this.state.directions) && (
                                <div className="px-4">
                                    <div className="mb-2 text-xl text-bold">Cooking Directions</div>
                                    <ol className="list-decimal">
                                        {this.state.directions.map((item, index) => (
                                            <li className="mb-4">{this.convertUnicode(item)}</li>
                                        ))}
                                    </ol>
                                </div>
                            )}
                        </div>
                    </div>}
            </div>
        );
    }
}

export default Search;