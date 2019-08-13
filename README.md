* 创建文件夹
    
    /flaskr
        /static
        /templates
        
* 创建应用模块并放置在 flaskr 目录下

        import os
        import sqlite3
        from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

