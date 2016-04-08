<%@ page language="java" contentType="text/html; charset=UTF-8"
  pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<%@ taglib prefix="green" tagdir="/WEB-INF/tags" %>

<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Green">
  <meta name="author" content="orangehat">
  
  <c:set value="${pageContext.request.contextPath}" var="path" scope="page" />

  <link href="http://cdn.staticfile.org/twitter-bootstrap/3.1.1/css/bootstrap.min.css" rel="stylesheet">
  <link href="${path}/css/bootstrap-wysihtml5.css" rel="stylesheet">
  
  <script src="${path}/js/wysihtml5-0.3.0.min.js"></script>
  <script src="http://cdn.staticfile.org/jquery/2.1.1-rc2/jquery.min.js"></script>
  <script src="http://cdn.staticfile.org/twitter-bootstrap/3.1.1/js/bootstrap.min.js"></script>
  <script src="${path}/js/bootstrap3-wysihtml5.js"></script>
  
  <link href="${path}/css/style.css" rel="stylesheet">
  
  <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
  <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
    <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
  <![endif]-->
  
  <title>Green|${topic.topicTitle}</title>
</head>

<body>
  <%@ include file="header.jsp" %>
  <div class="container content">
    <div class="tips">
	  <div class="tips-header"></div>
      <div class="tips-content-1">
	    <a class="btn btn-success" href="#form">發佈回覆</a>
	  </div>
	  <div class="tips-content-2">
	    <h2>小貼士</h2>
	    <div>${board.boardDesc}</div>
	  </div>
	</div> 	
    <div class="topic-title">${topic.topicTitle}</div>
    <div class="posts-wrapper">
      <c:forEach var="post" items="${pagedPost.result}">
   	    <div class="posts">
          <img class="avatar" src="${path}/images/avatar.png">
       	  <div class="post-info">
            <a href="#">${post.user.userName}</a>
		    <small>|</small>
       	    <small>創建：<fmt:formatDate pattern="yyyy-MM-dd" value="${post.createTime}"/></small>
            <a href="#"><span class="glyphicon glyphicon-thumbs-up"></span></a>
		    <a href="#"><span class="glyphicon glyphicon-share"></span></a>
       	  </div>
       	  <div class="post-text">
       	    ${post.postText}
       	  </div>
        </div>
      </c:forEach>  
	</div>
	<div class="clearfix"></div>
    <div class="pagebar">
      <green:PageBar 
        pageUrl="/board/listTopicPosts-${topic.topicId}.html"
        pageAttrKey="pagedPost"/>
    </div>	
  </div>
  <form id="form" class="container reply-post-form" action="<c:url value="/board/addPost.html" />" method="post">
    <div class="form-group reply-title">
      <input type="text" class="form-control" id="title" name="postTitle" placeholder="標題">
    </div>
    <textarea class="textarea form-control" name="postText" placeholder="輸入回覆內容 ..." style="width: 1140px; height: 200px">
    </textarea>
    <input type="hidden" name="boardId" value="${topic.boardId}"/>
    <input type="hidden" name="topic.topicId" value="${topic.topicId}"/>            
    <input class="submit-btn btn btn-primary btn-lg" type="submit" value="發佈">
  </form> 
  <%@ include file="footer.jsp" %>
  <script>
    $('.textarea').wysihtml5();
  </script>
  <script type="text/javascript" charset="utf-8">
    $(prettyPrint);
  </script>
</body>
</html>


