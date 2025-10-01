const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    entry: './assets/js/index.js',
    output: {
        path: path.resolve(__dirname, 'static'),
        filename: 'bundle.js',
        clean: true, // Nettoie le dossier de sortie
    },
    module: {
        rules: [
            // Règle pour les fichiers SCSS/CSS
            {
                test: /\.(scss|css)$/i,
                use: [
                    // Extrait le CSS dans des fichiers séparés
                    MiniCssExtractPlugin.loader,
                    // Traite les imports CSS et url()
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true,
                        }
                    },
                    // Ajoute les préfixes vendeur automatiquement
                    {
                        loader: 'postcss-loader',
                        options: {
                            postcssOptions: {
                                plugins: [
                                    require('autoprefixer'),
                                ],
                            },
                            sourceMap: true,
                        }
                    },
                    // Compile SCSS en CSS
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true,
                            sassOptions: {
                                includePaths: [
                                    path.resolve(__dirname, 'node_modules'),
                                    path.resolve(__dirname, 'static/scss'),
                                ],
                            },
                        }
                    },
                ],
            },
            // Règle pour les fonts et images
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/i,
                type: 'asset/resource',
                generator: {
                    filename: 'fonts/[name][ext]',
                },
            },
            {
                test: /\.(png|svg|jpg|jpeg|gif)$/i,
                type: 'asset/resource',
                generator: {
                    filename: 'images/[name][ext]',
                },
            },
        ],
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
        }),
        new MiniCssExtractPlugin({
            filename: 'styles.css',
            chunkFilename: '[id].css',
        }),
    ],
    resolve: {
        extensions: ['.js', '.scss', '.css'],
    },
    mode: 'development',
    devtool: 'source-map', // Source maps pour le debug
};