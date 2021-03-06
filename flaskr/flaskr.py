#Email:fanyucai1@126.com

import os,sys,re
sub=os.path.abspath(__file__)
dir_name=os.path.dirname(sub)
sys.path.append(dir_name)
import core
import subprocess
from flask import Flask, request, session, g, redirect, url_for, abort, render_template,flash,jsonify,make_response
from flask import redirect

###################创建了Flask类的实例
app=Flask(__name__)
###################给静态文件生成 URL，使用特殊的 'static' 端点名，这个文件应该存储在文件系统上的 static/style.css
#url_for('static', filename='style.css')
######################我们使用 route() 装饰器告诉 Flask 什么样的URL能触发我们的函数
##################并使用使用 render_template() 方法来渲染模板，Flask 会在 templates 文件夹里寻找 Jinja2 模板，之后教程中创建的模板将会放在这个文件夹里。

@app.route('/',methods=['GET','POST'])#http://127.0.0.1:5000/
def home():
    if request.method == 'POST' and request.form['cosmicID']!="":
        pattern=re.compile(r'(\d+)')
        id=pattern.findall(request.form['cosmicID'])
        return redirect("https://cancer.sanger.ac.uk/cosmic/mutation/overview?genome=37&id=%s"%(id[0]))
    return render_template('home.html')

@app.route('/knownCanonical', methods=['GET', 'POST'])
def knownCanonical():
    if request.method == 'POST' and request.form['Genename']!="":
        gene =request.form['Genename']
        clinvar,msk=core.known_Canonical.run(gene)
        return render_template('knownCanonical.html',Genename=gene,clinvar=clinvar,msk=msk)

@app.route('/hgvs', methods=['POST'])
def hgvs():
    if request.method == 'POST' and request.form['Var']!="":
        var = request.form['Var']
        nr, nt = core.hgvs_run.run(var)
        return render_template('hgvs.html', Var=var, Nr=nr, Nt=nt)

@app.route('/var_anno',methods=['POST'])
def var_anno():
    chr=request.form['Chr']
    pos=request.form['Pos']
    ref=request.form['Ref']
    alt=request.form['Alt']
    name,anno=core.var_anno.run(chr,pos,ref,alt)
    return render_template('var_anno.html',Chr=chr,Pos=pos,Ref=ref,Alt=alt,Name=name,Anno=anno)

@app.route('/site_retrieval',methods=['POST'])
def site_retrieval():
    chr = request.form['Chr']
    pos = request.form['Pos']
    chr,pos,gene,trans,details,chain,sequence,canoical_trans=core.site_retrieval.run(chr,pos)
    return render_template('site_retrieval.html',chr=chr,pos=pos,gene=gene,trans=trans,detail=details,chain=chain,sequence=sequence,canoical_trans=canoical_trans)

@app.route('/hotspot',methods=['POST'])
def hotsopt():
    chr = request.form['Chr']
    pos = request.form['Pos']
    ref=request.form['Ref']
    alt=request.form['Alt']
    string=core.hotspot.run(chr,pos,ref,alt)
    return render_template('hotspot.html',string=string)

if __name__ == '__main__':
    app.run(debug=True,host='192.168.1.120',port=100)
    #app.run(debug=True)