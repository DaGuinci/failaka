const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    entry: './assets/js/index.js',
    output: {
        path: path.resolve(__dirname, 'static'),
        filename: 'bundle.js',
        clean: true,
    },
    resolve: {
        extensions: ['.js', '.scss', '.css'],
        alias: {
            '@scss': path.resolve(__dirname, 'src/scss'),
        },
    },
    module: {
        rules: [
            {
                test: /\.(scss|css)$/i,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true,
                        }
                    },
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
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true,
                            sassOptions: {
                                includePaths: [
                                    path.resolve(__dirname, 'node_modules'),
                                    path.resolve(__dirname, 'src/scss'),
                                ],
                            },
                        }
                    },
                ],
            },
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
    mode: 'development',
    devtool: 'source-map',
};
