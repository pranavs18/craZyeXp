import pdb
from common import *
import json
from bson import json_util
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from stubs import authenticate # You need to define a decorator to do authenticate.

#Helper function
def AutoHttpResponse(code=200,res=None):
  if res and isinstance(res, dict):
    return HttpResponse(json_util.json.dumps(res,default=json_util.default),content_type = 'application/json')
  if code == 400:  
    res = {'res':None,'status':'error','msg':'400(Bad Request): '+str(res)} if res else {'res':None,'status':'error','msg':'400(Bad Request): required /invalid Paranmeter passed.'}
  if code == 501:  
    res = {'res':None,'status':'error','msg':'501(Not Implemented): '+str(res)} if res else {'res':None,'status':'error','msg':'501(Not Implemented)'}
  return HttpResponse(json_util.json.dumps(res,default=json_util.default),content_type = 'application/json') 


# This is Customized Stringto List converter separted by space or comma. result remove empty string.
#We support "[1,2,3]" or 'aa,bb,cc' or 'aa bb cc' to [1,2,3] Split Over , space or eval 
#
def str2List(s):
  if not s: return []
  if isinstance(s, list): return s;
  s=str(s)
  s = s.strip()
  try:
    if '[' in s:
      return eval(s)
    if ',' in s:
      return [ _i.strip() for _i in s.split(',') if _i]
    else:
      return [ _i for _i in s.split(' ') if _i ]
  except:
    D_LOG()
    print 'Error: eval Error: We support "[1,2,3]" or "aa,bb,cc" or "aa bb cc" to [1,2,3] Split Over , space or eval '
    return []
  
#Helper Function To Perse Advance Serach parmas
#Input : <a:b:c> => (a,b,c) >
def parseTriple(s):
  if not s: # for null check..
    return s
  res = [None,None,None]
  s = s.split(':')
  if len(s) >= 3:
    s[0] = '|' if s[0].lower() == 'or' else '&'   
    res = s[:3]
  elif len(s) == 2:
    res = ['|'] + s
  elif len(s) ==1:
    res = ['|','exact']+s
  if len(res[0]) == 0 : res[0] ="|"
  if len(res[1]) == 0 : res[1] ="exact"
  # rule for in and not in
  if res[1] in ['in','notin']:
    res[2] =  str2List(res[2])  
  return res
  


from .api import AuthorManager

@csrf_exempt
@authenticate
def ajax_Author(request,id=None):
  res=None
  
  #If the request is coming for get ..
  if request.method == 'GET':
    page=request.GET.get('page',None)
    limit=request.GET.get('limit',None)
    mv=request.GET.get('mv',None) # this is an Adding to get Mini View.. 
    name= request.GET.get('name') if request.GET.get('name','').strip() else None;life= request.GET.get('life') if request.GET.get('life','').strip() else None;mych= request.GET.get('mych') if request.GET.get('mych','').strip() else None;
    # NOTE: DONT POPULATE DEFAULT HERE.. WE WANT TO SEARCH HERE ONLY....
    #data Must be Normalized to required DataType..
    try:
      name = str(name) if( name) else name ;life = dict(life) if( life) else life ;mych = str2List(mych) if( mych) else mych ;
      
    except Exception,e:
      D_LOG()
      return AutoHttpResponse(400,getCustomException(e))
    # if Id is null, get the perticular Author or it's a search request
    if id is not None: 
      res= AuthorManager.getAuthor(id,mv=mv)
    else:
      # General Search request 
      id=request.GET.get('id',None) # We also support search based on ID.
      res= AuthorManager.searchAuthor(name=name,life=life,mych=mych,id=id,page=page,limit=limit,mv=mv  )
    
  #This is the implementation for POST request.
  elif request.method == 'POST':
    name= request.POST.get('name') if request.POST.get('name','').strip() else None;life= request.POST.get('life') if request.POST.get('life','').strip() else None;mych= request.POST.get('mych') if request.POST.get('mych','').strip() else None;   
    name=name if name else 'hari' ;life=life if life else {'house_rent':0,'food':0,'traval':0} ;mych=mych if mych else ['type1'] ;    
    #data Must be Normalized to required DataType..
    try:
      name = str(name) if( name) else name ;life = dict(life) if( life) else life ;mych = str2List(mych) if( mych) else mych ;      
    except Exception,e:
      D_LOG()
      return AutoHttpResponse(400,getCustomException(e))
    # Update request if id is not null. 
    if id is not None: 
      res=AuthorManager.updateAuthor(id=id,name=name,life=life,mych=mych,)
    else:
      # This is new entry request...
      res=AuthorManager.createAuthor(name=name,life=life,mych=mych,)
    
  # This is a Delete Request..
  elif request.method ==  'DELETE' and id is not None:
    res =AuthorManager.deleteAuthor(id)
  #Return the result after converting into json 
  return HttpResponse(json.dumps(res,default=json_util.default),content_type = 'application/json')


@csrf_exempt
@authenticate
def ajax_Author_Book(request,id=None):
  res=None
  #If the request is coming for get to all Book_set
  if request.method == 'GET':
      mv=request.GET.get('mv',None) # this is an Adding to get Mini View.. 
      res= AuthorManager.getAuthor_Book(id=id,mv=mv)

  #This is the implementation for POST request to add or delete Book
  elif request.method == 'POST':
    action=request.POST.get('action',None)
    if not action: return AutoHttpResponse(400,'Missing/Bad input: <action: add|remove > ?')
    book=str2List(request.POST.get('book',None))
    if not book : return AutoHttpResponse(400,'Missing/Bad input: <book: <id> > ?')
    # Update request if id is not null.
    if action.lower() == 'add':
      res=AuthorManager.addAuthor_Book(id=id,book = book)
    else:
      # do a delete action
      res=AuthorManager.removeAuthor_Book(id=id,book = book)

  #Return the result after converting into json
  return HttpResponse(json.dumps(res,default=json_util.default),content_type = 'application/json')



#   query_str_builder() Will build query_str from triples
def query_str_builder(key,v):
  if v[1] in ['tagin', 'tagnotin']:
    v2 = str2List(v[2])
    if v2[0][0] != '-':
      _m = ' '+v[0]+'( Q('+key+'__contains = "'+v2[0]+'") ' # BUG ? if we have two tag c and ccc, then ?
    else:
      _m = ' '+v[0]+'( ~Q('+key+'__contains = "'+v2[0][1:]+'") '
    for L in v2[1:]:
      if L[0] != '-':
        _m += ' & Q('+key+'__contains = "'+L+'") '
      else:
        _m += ' & ~Q('+key+'__contains = "'+L[1:]+'") '
    return _m +' ) '
    
  if v[1] in ['in', 'notin']:
    return v[0]+' Q('+key+'__'+v[1]+' = '+str(v[2])+') ' # this is a list in case of in/notin
  else:
    return v[0]+' Q('+key+'__'+v[1]+' = "'+str(v[2])+'") ' # else the v[2] will be String

@csrf_exempt
@authenticate
def ajax_Author_asearch(request): # We support POST only .
  res=None
  # This is basically a search by a tag or list items with given arguments
  if request.method == 'GET':
    return AutoHttpResponse(501)
  # This is basically a append to a list with given arguments
  elif request.method == 'POST':
    id=request.POST.get('id',None)    
    try: 
      #name = parseTriple(request.POST.get('name',None));life = parseTriple(request.POST.get('life',None));mych = parseTriple(request.POST.get('mych',None));
      non_field_params = ['orderBy','include','exclude']
      orderBy = request.POST.get('orderBy',None);
      if orderBy: orderBy = orderBy.split(',')
      include = request.POST.get('include',None);
      if include: include = include.split(',')
      exclude = request.POST.get('exclude',None);
      if exclude: exclude = exclude.split(',')
      
      #Define Query Strings.
      queryDict = dict(request.POST)
      for _x in non_field_params:
        if queryDict.has_key(_x):
          del queryDict[_x]
      #Now we should only have Database field.
      Qstr= ''
      for key, value in queryDict.iteritems():         
        if isinstance(value,str):
          v = parseTriple(value)
          if v: Qstr += query_str_builder(key,v)
        else:
          for v in value:
            v = parseTriple(v)
            if v: Qstr += query_str_builder(key,v)
      Qstr = Qstr[2:]         
      
    except:
      D_LOG()
      return AutoHttpResponse(400,'Wrong Pentameter format.') 	   
    
    try:
       res = AuthorManager.advSearchAuthor(id=id,query_str=Qstr,orderBy=orderBy,include=include,exclude=exclude)
    except:
      D_LOG()
      return AutoHttpResponse(400,'list item is not speared properly! Is your list field looks like: tags = [1,2,3] or tag1=%5B1%2C2%2C3%5D ?')
  return AutoHttpResponse(res=res)


@csrf_exempt
@authenticate
def ajax_Author_min_view(request):
  res=None
  if request.method == 'GET':
    page=request.GET.get('page',None)
    limit=request.GET.get('limit',None)
    res = AuthorManager.minViewAuthor(page=page,limit=limit)
    return AutoHttpResponse(res=res)
  else:
    return AutoHttpResponse(501)  


@csrf_exempt
@authenticate
def ajax_Author_read_only(request,id=None,cmd=None):
  res=None
  if request.method == 'GET':
    if (id ==None or cmd not in['setreadonly','removereadonly']):
      return AutoHttpResponse(200,'you must a input called /<table>/<id>/setreadonly or /<table>/<id>/removereadonly ')
    if cmd ==  'setreadonly':
      res = AuthorManager.set_Author_read_only(id)
    else:
      res = AuthorManager.unset_Author_read_only(id)
    return AutoHttpResponse(res=res)
  else:
    return AutoHttpResponse(501)  


from .api import PublicationManager

@csrf_exempt
@authenticate
def ajax_Publication(request,id=None):
  res=None
  
  #If the request is coming for get ..
  if request.method == 'GET':
    page=request.GET.get('page',None)
    limit=request.GET.get('limit',None)
    mv=request.GET.get('mv',None) # this is an Adding to get Mini View.. 
    name= request.GET.get('name') if request.GET.get('name','').strip() else None;accid= request.GET.get('accid') if request.GET.get('accid','').strip() else None;
    # NOTE: DONT POPULATE DEFAULT HERE.. WE WANT TO SEARCH HERE ONLY....
    #data Must be Normalized to required DataType..
    try:
      name = str(name) if( name) else name ;accid = int(accid) if( accid) else accid ;
      
    except Exception,e:
      D_LOG()
      return AutoHttpResponse(400,getCustomException(e))
    # if Id is null, get the perticular Publication or it's a search request
    if id is not None: 
      res= PublicationManager.getPublication(id,mv=mv)
    else:
      # General Search request 
      id=request.GET.get('id',None) # We also support search based on ID.
      res= PublicationManager.searchPublication(name=name,accid=accid,id=id,page=page,limit=limit,mv=mv  )
    
  #This is the implementation for POST request.
  elif request.method == 'POST':
    name= request.POST.get('name') if request.POST.get('name','').strip() else None;accid= request.POST.get('accid') if request.POST.get('accid','').strip() else None;   
    name=name if name else None ;accid=accid if accid else None ;    
    #data Must be Normalized to required DataType..
    try:
      name = str(name) if( name) else name ;accid = int(accid) if( accid) else accid ;      
    except Exception,e:
      D_LOG()
      return AutoHttpResponse(400,getCustomException(e))
    # Update request if id is not null. 
    if id is not None: 
      res=PublicationManager.updatePublication(id=id,name=name,accid=accid,)
    else:
      # This is new entry request...
      res=PublicationManager.createPublication(name=name,accid=accid,)
    
  # This is a Delete Request..
  elif request.method ==  'DELETE' and id is not None:
    res =PublicationManager.deletePublication(id)
  #Return the result after converting into json 
  return HttpResponse(json.dumps(res,default=json_util.default),content_type = 'application/json')


@csrf_exempt
@authenticate
def ajax_Publication_Book(request,id=None):
  res=None
  #If the request is coming for get to all Book_set
  if request.method == 'GET':
      mv=request.GET.get('mv',None) # this is an Adding to get Mini View.. 
      res= PublicationManager.getPublication_Book(id=id,mv=mv)

  #This is the implementation for POST request to add or delete Book
  elif request.method == 'POST':
    action=request.POST.get('action',None)
    if not action: return AutoHttpResponse(400,'Missing/Bad input: <action: add|remove > ?')
    book=str2List(request.POST.get('book',None))
    if not book : return AutoHttpResponse(400,'Missing/Bad input: <book: <id> > ?')
    # Update request if id is not null.
    if action.lower() == 'add':
      res=PublicationManager.addPublication_Book(id=id,book = book)
    else:
      # do a delete action
      res=PublicationManager.removePublication_Book(id=id,book = book)

  #Return the result after converting into json
  return HttpResponse(json.dumps(res,default=json_util.default),content_type = 'application/json')



#   query_str_builder() Will build query_str from triples
def query_str_builder(key,v):
  if v[1] in ['tagin', 'tagnotin']:
    v2 = str2List(v[2])
    if v2[0][0] != '-':
      _m = ' '+v[0]+'( Q('+key+'__contains = "'+v2[0]+'") ' # BUG ? if we have two tag c and ccc, then ?
    else:
      _m = ' '+v[0]+'( ~Q('+key+'__contains = "'+v2[0][1:]+'") '
    for L in v2[1:]:
      if L[0] != '-':
        _m += ' & Q('+key+'__contains = "'+L+'") '
      else:
        _m += ' & ~Q('+key+'__contains = "'+L[1:]+'") '
    return _m +' ) '
    
  if v[1] in ['in', 'notin']:
    return v[0]+' Q('+key+'__'+v[1]+' = '+str(v[2])+') ' # this is a list in case of in/notin
  else:
    return v[0]+' Q('+key+'__'+v[1]+' = "'+str(v[2])+'") ' # else the v[2] will be String

@csrf_exempt
@authenticate
def ajax_Publication_asearch(request): # We support POST only .
  res=None
  # This is basically a search by a tag or list items with given arguments
  if request.method == 'GET':
    return AutoHttpResponse(501)
  # This is basically a append to a list with given arguments
  elif request.method == 'POST':
    id=request.POST.get('id',None)    
    try: 
      #name = parseTriple(request.POST.get('name',None));accid = parseTriple(request.POST.get('accid',None));
      non_field_params = ['orderBy','include','exclude']
      orderBy = request.POST.get('orderBy',None);
      if orderBy: orderBy = orderBy.split(',')
      include = request.POST.get('include',None);
      if include: include = include.split(',')
      exclude = request.POST.get('exclude',None);
      if exclude: exclude = exclude.split(',')
      
      #Define Query Strings.
      queryDict = dict(request.POST)
      for _x in non_field_params:
        if queryDict.has_key(_x):
          del queryDict[_x]
      #Now we should only have Database field.
      Qstr= ''
      for key, value in queryDict.iteritems():         
        if isinstance(value,str):
          v = parseTriple(value)
          if v: Qstr += query_str_builder(key,v)
        else:
          for v in value:
            v = parseTriple(v)
            if v: Qstr += query_str_builder(key,v)
      Qstr = Qstr[2:]         
      
    except:
      D_LOG()
      return AutoHttpResponse(400,'Wrong Pentameter format.') 	   
    
    try:
       res = PublicationManager.advSearchPublication(id=id,query_str=Qstr,orderBy=orderBy,include=include,exclude=exclude)
    except:
      D_LOG()
      return AutoHttpResponse(400,'list item is not speared properly! Is your list field looks like: tags = [1,2,3] or tag1=%5B1%2C2%2C3%5D ?')
  return AutoHttpResponse(res=res)


@csrf_exempt
@authenticate
def ajax_Publication_min_view(request):
  res=None
  if request.method == 'GET':
    page=request.GET.get('page',None)
    limit=request.GET.get('limit',None)
    res = PublicationManager.minViewPublication(page=page,limit=limit)
    return AutoHttpResponse(res=res)
  else:
    return AutoHttpResponse(501)  


from .api import TOCManager

@csrf_exempt
@authenticate
def ajax_TOC(request,id=None):
  res=None
  
  #If the request is coming for get ..
  if request.method == 'GET':
    page=request.GET.get('page',None)
    limit=request.GET.get('limit',None)
    mv=request.GET.get('mv',None) # this is an Adding to get Mini View.. 
    name= request.GET.get('name') if request.GET.get('name','').strip() else None;
    # NOTE: DONT POPULATE DEFAULT HERE.. WE WANT TO SEARCH HERE ONLY....
    #data Must be Normalized to required DataType..
    try:
      name = str(name) if( name) else name ;
      
    except Exception,e:
      D_LOG()
      return AutoHttpResponse(400,getCustomException(e))
    # if Id is null, get the perticular TOC or it's a search request
    if id is not None: 
      res= TOCManager.getTOC(id,mv=mv)
    else:
      # General Search request 
      id=request.GET.get('id',None) # We also support search based on ID.
      res= TOCManager.searchTOC(name=name,id=id,page=page,limit=limit,mv=mv  )
    
  #This is the implementation for POST request.
  elif request.method == 'POST':
    name= request.POST.get('name') if request.POST.get('name','').strip() else None;   
    name=name if name else None ;    
    #data Must be Normalized to required DataType..
    try:
      name = str(name) if( name) else name ;      
    except Exception,e:
      D_LOG()
      return AutoHttpResponse(400,getCustomException(e))
    # Update request if id is not null. 
    if id is not None: 
      res=TOCManager.updateTOC(id=id,name=name,)
    else:
      # This is new entry request...
      res=TOCManager.createTOC(name=name,)
    
  # This is a Delete Request..
  elif request.method ==  'DELETE' and id is not None:
    res =TOCManager.deleteTOC(id)
  #Return the result after converting into json 
  return HttpResponse(json.dumps(res,default=json_util.default),content_type = 'application/json')


@csrf_exempt
@authenticate
def ajax_TOC_Book(request,id=None):
  res=None
  #If the request is coming for get to all Book_set
  if request.method == 'GET':
      mv=request.GET.get('mv',None) # this is an Adding to get Mini View.. 
      res= TOCManager.getTOC_Book(id=id,mv=mv)

  #This is the implementation for POST request to add or delete Book
  elif request.method == 'POST':
    action=request.POST.get('action',None)
    if not action: return AutoHttpResponse(400,'Missing/Bad input: <action: add|remove > ?')
    book=str2List(request.POST.get('book',None))
    if not book : return AutoHttpResponse(400,'Missing/Bad input: <book: <id> > ?')
    # Update request if id is not null.
    if action.lower() == 'add':
      res=TOCManager.addTOC_Book(id=id,book = book)
    else:
      # do a delete action
      res=TOCManager.removeTOC_Book(id=id,book = book)

  #Return the result after converting into json
  return HttpResponse(json.dumps(res,default=json_util.default),content_type = 'application/json')



#   query_str_builder() Will build query_str from triples
def query_str_builder(key,v):
  if v[1] in ['tagin', 'tagnotin']:
    v2 = str2List(v[2])
    if v2[0][0] != '-':
      _m = ' '+v[0]+'( Q('+key+'__contains = "'+v2[0]+'") ' # BUG ? if we have two tag c and ccc, then ?
    else:
      _m = ' '+v[0]+'( ~Q('+key+'__contains = "'+v2[0][1:]+'") '
    for L in v2[1:]:
      if L[0] != '-':
        _m += ' & Q('+key+'__contains = "'+L+'") '
      else:
        _m += ' & ~Q('+key+'__contains = "'+L[1:]+'") '
    return _m +' ) '
    
  if v[1] in ['in', 'notin']:
    return v[0]+' Q('+key+'__'+v[1]+' = '+str(v[2])+') ' # this is a list in case of in/notin
  else:
    return v[0]+' Q('+key+'__'+v[1]+' = "'+str(v[2])+'") ' # else the v[2] will be String

@csrf_exempt
@authenticate
def ajax_TOC_asearch(request): # We support POST only .
  res=None
  # This is basically a search by a tag or list items with given arguments
  if request.method == 'GET':
    return AutoHttpResponse(501)
  # This is basically a append to a list with given arguments
  elif request.method == 'POST':
    id=request.POST.get('id',None)    
    try: 
      #name = parseTriple(request.POST.get('name',None));
      non_field_params = ['orderBy','include','exclude']
      orderBy = request.POST.get('orderBy',None);
      if orderBy: orderBy = orderBy.split(',')
      include = request.POST.get('include',None);
      if include: include = include.split(',')
      exclude = request.POST.get('exclude',None);
      if exclude: exclude = exclude.split(',')
      
      #Define Query Strings.
      queryDict = dict(request.POST)
      for _x in non_field_params:
        if queryDict.has_key(_x):
          del queryDict[_x]
      #Now we should only have Database field.
      Qstr= ''
      for key, value in queryDict.iteritems():         
        if isinstance(value,str):
          v = parseTriple(value)
          if v: Qstr += query_str_builder(key,v)
        else:
          for v in value:
            v = parseTriple(v)
            if v: Qstr += query_str_builder(key,v)
      Qstr = Qstr[2:]         
      
    except:
      D_LOG()
      return AutoHttpResponse(400,'Wrong Pentameter format.') 	   
    
    try:
       res = TOCManager.advSearchTOC(id=id,query_str=Qstr,orderBy=orderBy,include=include,exclude=exclude)
    except:
      D_LOG()
      return AutoHttpResponse(400,'list item is not speared properly! Is your list field looks like: tags = [1,2,3] or tag1=%5B1%2C2%2C3%5D ?')
  return AutoHttpResponse(res=res)


@csrf_exempt
@authenticate
def ajax_TOC_min_view(request):
  res=None
  if request.method == 'GET':
    page=request.GET.get('page',None)
    limit=request.GET.get('limit',None)
    res = TOCManager.minViewTOC(page=page,limit=limit)
    return AutoHttpResponse(res=res)
  else:
    return AutoHttpResponse(501)  


from .api import BookManager

@csrf_exempt
@authenticate
def ajax_Book(request,id=None):
  res=None
  
  #If the request is coming for get ..
  if request.method == 'GET':
    page=request.GET.get('page',None)
    limit=request.GET.get('limit',None)
    mv=request.GET.get('mv',None) # this is an Adding to get Mini View.. 
    name= request.GET.get('name') if request.GET.get('name','').strip() else None;authors= request.GET.get('authors') if request.GET.get('authors','').strip() else None;reg= request.GET.get('reg') if request.GET.get('reg','').strip() else None;publication= request.GET.get('publication') if request.GET.get('publication','').strip() else None;toc= request.GET.get('toc') if request.GET.get('toc','').strip() else None;tag1= request.GET.get('tag1') if request.GET.get('tag1','').strip() else None;tag2= request.GET.get('tag2') if request.GET.get('tag2','').strip() else None;mych= request.GET.get('mych') if request.GET.get('mych','').strip() else None;mych2= request.GET.get('mych2') if request.GET.get('mych2','').strip() else None;
    # NOTE: DONT POPULATE DEFAULT HERE.. WE WANT TO SEARCH HERE ONLY....
    #data Must be Normalized to required DataType..
    try:
      name = str(name) if( name) else name ;authors = str2List(authors) if( authors) else authors ;reg = int(reg) if( reg) else reg ;publication = str2List(publication) if( publication) else publication ;toc = int(toc) if( toc) else toc ;tag1 = str2List(tag1) if( tag1) else tag1 ;tag2 = str2List(tag2) if( tag2) else tag2 ;mych = str2List(mych) if( mych) else mych ;mych2 = str2List(mych2) if( mych2) else mych2 ;
      
    except Exception,e:
      D_LOG()
      return AutoHttpResponse(400,getCustomException(e))
    # if Id is null, get the perticular Book or it's a search request
    if id is not None: 
      res= BookManager.getBook(id,mv=mv)
    else:
      # General Search request 
      id=request.GET.get('id',None) # We also support search based on ID.
      res= BookManager.searchBook(name=name,authors=authors,reg=reg,publication=publication,toc=toc,tag1=tag1,tag2=tag2,mych=mych,mych2=mych2,id=id,page=page,limit=limit,mv=mv  )
    
  #This is the implementation for POST request.
  elif request.method == 'POST':
    name= request.POST.get('name') if request.POST.get('name','').strip() else None;authors= request.POST.get('authors') if request.POST.get('authors','').strip() else None;reg= request.POST.get('reg') if request.POST.get('reg','').strip() else None;publication= request.POST.get('publication') if request.POST.get('publication','').strip() else None;toc= request.POST.get('toc') if request.POST.get('toc','').strip() else None;tag1= request.POST.get('tag1') if request.POST.get('tag1','').strip() else None;tag2= request.POST.get('tag2') if request.POST.get('tag2','').strip() else None;mych= request.POST.get('mych') if request.POST.get('mych','').strip() else None;mych2= request.POST.get('mych2') if request.POST.get('mych2','').strip() else None;   
    name=name if name else None ;authors=authors if authors else None ;reg=reg if reg else None ;publication=publication if publication else None ;toc=toc if toc else None ;tag1=tag1 if tag1 else None ;tag2=tag2 if tag2 else None ;mych=mych if mych else None ;mych2=mych2 if mych2 else None ;    
    #data Must be Normalized to required DataType..
    try:
      name = str(name) if( name) else name ;authors = str2List(authors) if( authors) else authors ;reg = int(reg) if( reg) else reg ;publication = str2List(publication) if( publication) else publication ;toc = int(toc) if( toc) else toc ;tag1 = str2List(tag1) if( tag1) else tag1 ;tag2 = str2List(tag2) if( tag2) else tag2 ;mych = str2List(mych) if( mych) else mych ;mych2 = str2List(mych2) if( mych2) else mych2 ;      
    except Exception,e:
      D_LOG()
      return AutoHttpResponse(400,getCustomException(e))
    # Update request if id is not null. 
    if id is not None: 
      res=BookManager.updateBook(id=id,name=name,authors=authors,reg=reg,publication=publication,toc=toc,tag1=tag1,tag2=tag2,mych=mych,mych2=mych2,)
    else:
      # This is new entry request...
      res=BookManager.createBook(name=name,authors=authors,reg=reg,publication=publication,toc=toc,tag1=tag1,tag2=tag2,mych=mych,mych2=mych2,)
    
  # This is a Delete Request..
  elif request.method ==  'DELETE' and id is not None:
    res =BookManager.deleteBook(id)
  #Return the result after converting into json 
  return HttpResponse(json.dumps(res,default=json_util.default),content_type = 'application/json')


@csrf_exempt
@authenticate
def ajax_Book_TOC(request,id=None):
  res=None
  #If the request is coming for get to all TOC_set
  if request.method == 'GET':
      mv=request.GET.get('mv',None) # this is an Adding to get Mini View.. 
      res= BookManager.getBook_TOC(id=id,mv=mv)

  #This is the implementation for POST request to add or delete TOC
  elif request.method == 'POST':
    action=request.POST.get('action',None)
    if not action: return AutoHttpResponse(400,'Missing/Bad input: <action: add|remove > ?')
    toc=str2List(request.POST.get('toc',None))
    if not toc : return AutoHttpResponse(400,'Missing/Bad input: <toc: <id> > ?')
    # Update request if id is not null.
    if action.lower() == 'add':
      res=BookManager.addBook_TOC(id=id,toc = toc)
    else:
      # do a delete action
      res=BookManager.removeBook_TOC(id=id,toc = toc)

  #Return the result after converting into json
  return HttpResponse(json.dumps(res,default=json_util.default),content_type = 'application/json')



@csrf_exempt
@authenticate
def ajax_Book_Author(request,id=None):
  res=None
  #If the request is coming for get to all Author_set
  if request.method == 'GET':
      mv=request.GET.get('mv',None) # this is an Adding to get Mini View.. 
      res= BookManager.getBook_Author(id=id,mv=mv)

  #This is the implementation for POST request to add or delete Author
  elif request.method == 'POST':
    action=request.POST.get('action',None)
    if not action: return AutoHttpResponse(400,'Missing/Bad input: <action: add|remove > ?')
    authors=str2List(request.POST.get('authors',None))
    if not authors : return AutoHttpResponse(400,'Missing/Bad input: <authors: <id> > ?')
    # Update request if id is not null.
    if action.lower() == 'add':
      res=BookManager.addBook_Author(id=id,authors = authors)
    else:
      # do a delete action
      res=BookManager.removeBook_Author(id=id,authors = authors)

  #Return the result after converting into json
  return HttpResponse(json.dumps(res,default=json_util.default),content_type = 'application/json')



@csrf_exempt
@authenticate
def ajax_Book_Publication(request,id=None):
  res=None
  #If the request is coming for get to all Publication_set
  if request.method == 'GET':
      mv=request.GET.get('mv',None) # this is an Adding to get Mini View.. 
      res= BookManager.getBook_Publication(id=id,mv=mv)

  #This is the implementation for POST request to add or delete Publication
  elif request.method == 'POST':
    action=request.POST.get('action',None)
    if not action: return AutoHttpResponse(400,'Missing/Bad input: <action: add|remove > ?')
    publication=str2List(request.POST.get('publication',None))
    if not publication : return AutoHttpResponse(400,'Missing/Bad input: <publication: <id> > ?')
    # Update request if id is not null.
    if action.lower() == 'add':
      res=BookManager.addBook_Publication(id=id,publication = publication)
    else:
      # do a delete action
      res=BookManager.removeBook_Publication(id=id,publication = publication)

  #Return the result after converting into json
  return HttpResponse(json.dumps(res,default=json_util.default),content_type = 'application/json')



@csrf_exempt
@authenticate
def ajax_Book_list(request,id=None,):
  res=None
  # This is basically a search by a tag or list items with given arguments
  if request.method == 'GET':
    return AutoHttpResponse(501)
  # This is basically a append to a list with given arguments
  elif request.method == 'POST':
    action=request.POST.get('action',None)
    if action not in ['APPEND', 'REMOVE', 'SEARCH'] : return AutoHttpResponse(400,'id missing ! your post data must have action = APPEND or REMOVE or SEARCH ?')     
    if not id and action != 'SEARCH' : return AutoHttpResponse(400,'id missing ! is your urls looks like http://192.168.56.101:7777/api/Author/1/list/ ?')   

    try:
      tag1 = eval(request.POST.get('tag1','[]'));tag2 = eval(request.POST.get('tag2','[]'));
      if action == 'APPEND':
        res = BookManager.appendListBook(id,tag1=tag1,tag2=tag2,)
      elif action == 'REMOVE':
        res = BookManager.removeListBook(id,tag1=tag1,tag2=tag2,)
      elif action == 'SEARCH':
        res = BookManager.searchListBook(tag1=tag1,tag2=tag2,)
    except:
      D_LOG()
      return AutoHttpResponse(400,'list item is not speared properly! Is your list field looks like: tags = [1,2,3] or tag1=%5B1%2C2%2C3%5D ?')

  #Return the result after converting into json
  return HttpResponse(json.dumps(res,default=json_util.default),content_type = 'application/json')


#   query_str_builder() Will build query_str from triples
def query_str_builder(key,v):
  if v[1] in ['tagin', 'tagnotin']:
    v2 = str2List(v[2])
    if v2[0][0] != '-':
      _m = ' '+v[0]+'( Q('+key+'__contains = "'+v2[0]+'") ' # BUG ? if we have two tag c and ccc, then ?
    else:
      _m = ' '+v[0]+'( ~Q('+key+'__contains = "'+v2[0][1:]+'") '
    for L in v2[1:]:
      if L[0] != '-':
        _m += ' & Q('+key+'__contains = "'+L+'") '
      else:
        _m += ' & ~Q('+key+'__contains = "'+L[1:]+'") '
    return _m +' ) '
    
  if v[1] in ['in', 'notin']:
    return v[0]+' Q('+key+'__'+v[1]+' = '+str(v[2])+') ' # this is a list in case of in/notin
  else:
    return v[0]+' Q('+key+'__'+v[1]+' = "'+str(v[2])+'") ' # else the v[2] will be String

@csrf_exempt
@authenticate
def ajax_Book_asearch(request): # We support POST only .
  res=None
  # This is basically a search by a tag or list items with given arguments
  if request.method == 'GET':
    return AutoHttpResponse(501)
  # This is basically a append to a list with given arguments
  elif request.method == 'POST':
    id=request.POST.get('id',None)    
    try: 
      #name = parseTriple(request.POST.get('name',None));authors = parseTriple(request.POST.get('authors',None));reg = parseTriple(request.POST.get('reg',None));publication = parseTriple(request.POST.get('publication',None));toc = parseTriple(request.POST.get('toc',None));tag1 = parseTriple(request.POST.get('tag1',None));tag2 = parseTriple(request.POST.get('tag2',None));mych = parseTriple(request.POST.get('mych',None));mych2 = parseTriple(request.POST.get('mych2',None));
      non_field_params = ['orderBy','include','exclude']
      orderBy = request.POST.get('orderBy',None);
      if orderBy: orderBy = orderBy.split(',')
      include = request.POST.get('include',None);
      if include: include = include.split(',')
      exclude = request.POST.get('exclude',None);
      if exclude: exclude = exclude.split(',')
      
      #Define Query Strings.
      queryDict = dict(request.POST)
      for _x in non_field_params:
        if queryDict.has_key(_x):
          del queryDict[_x]
      #Now we should only have Database field.
      Qstr= ''
      for key, value in queryDict.iteritems():         
        if isinstance(value,str):
          v = parseTriple(value)
          if v: Qstr += query_str_builder(key,v)
        else:
          for v in value:
            v = parseTriple(v)
            if v: Qstr += query_str_builder(key,v)
      Qstr = Qstr[2:]         
      
    except:
      D_LOG()
      return AutoHttpResponse(400,'Wrong Pentameter format.') 	   
    
    try:
       res = BookManager.advSearchBook(id=id,query_str=Qstr,orderBy=orderBy,include=include,exclude=exclude)
    except:
      D_LOG()
      return AutoHttpResponse(400,'list item is not speared properly! Is your list field looks like: tags = [1,2,3] or tag1=%5B1%2C2%2C3%5D ?')
  return AutoHttpResponse(res=res)


@csrf_exempt
@authenticate
def ajax_Book_min_view(request):
  res=None
  if request.method == 'GET':
    page=request.GET.get('page',None)
    limit=request.GET.get('limit',None)
    res = BookManager.minViewBook(page=page,limit=limit)
    return AutoHttpResponse(res=res)
  else:
    return AutoHttpResponse(501)  


@csrf_exempt
@authenticate
def ajax_Book_quick_search(request):
  res=None
  if request.method == 'GET':
    page=request.GET.get('page',None)
    limit=request.GET.get('limit',None)
    q=request.GET.get('q',None)
    if not q:
      return AutoHttpResponse(200,'you must a input called ?q=abcd') 
    res = BookManager.getBook_quick_search(q=q,page=page,limit=limit)
    return AutoHttpResponse(res=res)
  else:
    return AutoHttpResponse(501)  

